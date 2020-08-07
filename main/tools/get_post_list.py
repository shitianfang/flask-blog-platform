#当前问题
#1，翻页到最后三种情况，一种是404状态()，一种是200正常但是无标题，一种是200正常但是有标题仍然显示最后一页

from pyquery import PyQuery as pq
import urllib,sys

def get_article_list(url,page_rule,titles_selector,links_selector,page_second_num,encoding="utf-8"):

    #如果为空则文章不分页
    if page_rule:
        #预处理
        if "<num>" not in page_rule:
            raise ValueError("<num>不在翻页网址中")     
    
    doc=pq(url,encoding=encoding)
    titles=[t.text() for t in doc(titles_selector).items()]
    links=[l.attr("href") for l in doc(links_selector).items()]

    if not titles:
        raise ValueError("未获取到文章标题")

    if not links:
        raise ValueError("未获取到文章链接")
    
    i=2
    last_cache=[]

    print("启动循环加载")

    try:
        while True:
            doc=pq(page_rule.replace("<num>",str(i)),encoding=encoding)
            this_title=[t.text() for t in doc(titles_selector).items()]
            this_link=[l.attr("href") for l in doc(links_selector).items()]
            
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

    
    article_zip=zip(titles,links)    
    return article_zip


def print_article_list(a_data):
    for t,l in a_data:
        print(t,l)
        




if __name__=="__main__":
    data={
        "url":"https://www.vinoca.org/",
        "page_rule":"https://www.vinoca.org/page/<num>/",
        "titles_selector":".content h2 a",
        "links_selector":".content h2 a",
        "page_second_num":"2"
    }

    try:
        print_article_list(get_article_list(**data))
    except ValueError as e:
        print(repr(e))
    except urllib.error.HTTPError as e:
        print(repr(e))
    except:
        print("未知错误：", sys.exc_info()[0])

    # try:
    #     print(pq("http://www.yangxg.com/6"))
    # except urllib.error.HTTPError as e:
    #     print(repr(e))
    