from os import link
from main.start import db,celery
from main.models import Post,Blog
from pyquery import PyQuery as pq
from main.mail import send_crawl_mail
import urllib,hashlib,json,requests,feedparser

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

def _set_task_progress(self,pr):
    self.update_state(state="开始处理",meta={'total':pr})
   

def _deal_links(links,abs_url):
    new_links=[]
    for link in links:
        if link[:4]=="http":
            new_links.append(link)
        else:
            new_links.append(abs_url+link)
    return new_links

#当前问题
#1，翻页到最后三种情况，一种是404状态()，一种是200正常但是无标题，一种是200正常但是有标题仍然显示最后一页
def get_article_list(self,abs_url,p_home,p_page,p_title,p_link,page_second_num=2,encoding="utf-8"):

    abs_url=abs_url if abs_url[-1]=="/" else abs_url+"/"
    print(abs_url)
    #如果为空则文章不分页
    if p_page:
        #预处理
        if "<num>" not in p_page:
            raise ValueError("<num>不在翻页网址中，请检查分页规则是否填写正确，若无分页则留空即可")     
    
    doc=pq(requests.get(p_home,headers=headers).text)
    titles=[t.text() for t in doc(p_title).items()]
    links=_deal_links([l.attr("href") for l in doc(p_link).items()],abs_url)

    self.update_state(state="开始处理",meta={'total':10})

    if not titles:
        raise ValueError("未获取到文章标题，请检查标题选择器是否填写正确")

    if not links:
        raise ValueError("未获取到文章链接，请检查链接选择器是否填写正确")
    
    i=2
    last_cache=[]

    print("启动循环加载")

    if p_page:
        try:
            while True:
                doc=pq(requests.get(p_page.replace("<num>",str(i)),headers=headers).text)
                this_title=[t.text() for t in doc(p_title).items()]
                this_link=_deal_links([l.attr("href") for l in doc(p_link).items()],abs_url)
                
                if i>2:
                    _set_task_progress(self=self,pr=30+i if 30+i<50 else 49)
                else:
                    _set_task_progress(self=self,pr=i*10)
    
                # print(this_title)
    
                if not this_title:
                    print("未获取到标题")
                    break
                
                if not this_link:
                    print("未获取到链接")
                    break
                
                if this_title==last_cache:
                    print("两次得到相同标题")
                    break
                
                last_cache=this_title
    
                titles.extend(this_title)
                links.extend(this_link)
    
                i+=1
    
        except urllib.error.HTTPError as e:
            print(repr(e))
        except :
            print("未知错误")

    
    article_zip=zip(titles,links)    
    
    return list(article_zip)


def get_article_body(url,body_rule,encoding="utf-8"):
    doc=pq(requests.get(url,headers=headers).text)
    body_data=doc(body_rule).html()
    if not body_data:
        raise ValueError("未获取到文章正文内容，请检查正文选择器是否填写正确")
    return body_data

def hash_md5_text(text):
    return hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()

def create_md5s_json(urls):
    md5s=[]
    for url in urls:
        md5s.append(hash_md5_text(url))
    return json.dumps(md5s)


#此处是在lauch任务中启动的函数
# @shared_task(bind=True)
@celery.task(bind=True)
def crwal_blog_data(self,blog_id,ismanual=False):

    #初始化数据集
    _set_task_progress(self=self,pr=1)
    blog=Blog.query.filter_by(id=blog_id).first()
    a_list_rule={
        "p_home":blog.crawl.get("p_home"),
        "p_page":blog.crawl.get("p_page"),
        "p_title":blog.crawl.get("p_title"),
        "p_link":blog.crawl.get("p_link")
    }

    #加载urlset
    url_set_json=blog.crawl.urlset
    url_set=None
    if url_set_json:
        url_set=set(json.loads(url_set_json))

    #爬虫执行
    a_list=get_article_list(self=self,abs_url=blog.homepage,**a_list_rule)

    #爬虫处理
    new_a_list=a_list
    if url_set:
        new_a_list=[(t,l) for t,l in a_list if hash_md5_text(l) not in url_set]

    #进度操作
    _set_task_progress(self=self,pr=50)
    a_len=len(new_a_list)

    #保存文章列表
    if blog.big_categor_id==1:
        recommend=True
    else:
        recommend=False
        
    save_post=[Post(url=l,title=t,blog=blog,recommend=recommend) for t,l in new_a_list]
    db.session.add_all(save_post)
    #保存url_md5
    blog.crawl.urlset=create_md5s_json([l for t,l in a_list])
    db.session.commit()



    #获取正文Body
    i=0
    for p in save_post:
        i+=1
        a_body=get_article_body(p.url,blog.crawl.get("p_body"))   
        p.body=a_body 
        p.digest=pq(a_body).text()[:300]
        _set_task_progress(self=self,pr=50+50*i//a_len)

    #完成结束
    blog.crawl.taskdone=True
    db.session.commit()
    _set_task_progress(self=self,pr=100)


    #执行完后发送邮件通知用户
    # if ismanual:
    #     send_crawl_mail(blog)

@celery.task(bind=True)
def crawl_rrs_data(self,blog_id):

    _set_task_progress(self=self,pr=1)

    
    blog=Blog.query.filter_by(id=blog_id).first()
    url_set_json=blog.crawl.urlset
    url_set=None
    if url_set_json:
        url_set=set(json.loads(url_set_json))

    _set_task_progress(self=self,pr=10)

    d=feedparser.parse(blog.crawl.rrs)
    print(d)
    print(blog.crawl.rrs)
    link_list=[]
    entlen=len(d.entries)
    i=1
    for e in d.entries:
        print(e.title)
        if url_set:
            if hash_md5_text(e.link) in url_set:
                continue
        db.session.add(Post(url=e.link,title=e.title,body=e.content[0]["value"],blog=blog,digest=pq(e.content[0]["value"]).text()[:300]))
        link_list.append(e.link)
        _set_task_progress(self=self,pr=10+90*i/entlen)
        i+=1

    blog.crawl.urlset=create_md5s_json(link_list)
    blog.crawl.taskdone=True
    db.session.commit()

    _set_task_progress(self=self,pr=100)
    

   



