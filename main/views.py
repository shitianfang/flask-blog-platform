from main.start import app,db
from flask import render_template,url_for,g,request,flash,redirect,send_from_directory,session,make_response,jsonify
from main.models import Blog,BigCategor,Post,Crawl,load_blog
from main.cache import categors
from main.forms import BlogForm,CrawlForm,RRSForm,LoginForm
from main.tool import random_filename,comma_replace
from flask_login import current_user,login_user,logout_user,login_required
from main.mail import send_login_mail
import os
from main.tasks import crwal_blog_data,crawl_rrs_data
from main.tool import deal_url_end
from sqlalchemy.sql.expression import func

#函数调用


#请求钩子
@app.before_request
def data_transfer():
    g.categors=categors

#处理页面
@app.route('/')
@app.route('/index/')
def index():
    flash("团队招募一名前端（BootStrap4）设计人员，有意加QQ群：1126037372",category="notice")
    var_dict={
        "pre_row_limit":app.config["BLOGS_PER_ROW"],
        "pre_cate_limit":app.config["BLOGS_PER_CATE"],
        "categors":BigCategor.query.all()
    }

    return render_template("index.html",**var_dict)

#主要要先提交blog才能调用
def init_blog_crawl(blog):
    plat=blog.platform

    if plat=="person":
        return

    if plat=="csdn":
        p_home=blog.homepage
        p_home=p_home if p_home[8:12]=="blog" else p_home[:8]+"blog"+p_home[10:]
        _var={
            "p_home":p_home,
            "p_page":deal_url_end(p_home)+"article/list/<num>",
            "p_title":".article-item-box h4 a",
            "p_link":".article-item-box h4 a",
            "p_body":"#article_content"
        }
        blog.crawl=Crawl(**_var)        

    elif plat=="cnblogs":
        p_home=deal_url_end(blog.homepage)
        p_home=p_home if p_home[-2:]=="p/" else deal_url_end(p_home)+"p/"
        _var={
            "p_home":p_home,
            "p_page":deal_url_end(p_home)+"?page=<num>",
            "p_title":".postTitl2 a",
            "p_link":".postTitl2 a",
            "p_body":"#cnblogs_post_body"
        }
        blog.crawl=Crawl(**_var) 
    
    db.session.commit()
    task=crwal_blog_data.delay(blog.id,True)
    blog.crawl.taskid=task.id    
    blog.crawl.taskdone=False
    db.session.commit()
    flash("已提交博客文章处理任务，请到后台-文章列表查看")

@app.route('/upload/',methods=['GET','POST'])
def upload_blog():
    form=BlogForm()
    if form.validate_on_submit():
        #文件处理
        f=form.logo.data
        filename=random_filename(f.filename)
        
        if not form.email.data:
            form.email.data=None

        var_blog={
            "name":form.name.data,
            "email":form.email.data,
            "homepage":form.url.data,
            # "about":form.about.data,
            "logo":filename,
            "big_categor":BigCategor.query.filter_by(id=form.categor.data).first(),
            # "keyword":comma_replace(form.keyword.data)
            "platform":form.platform.data
        }
        
        blog=Blog(**var_blog)
        db.session.add(blog)

        f.save(os.path.join(app.config['UPLOAD_LOGO_PATH'],filename))

        db.session.commit()

        flash('提交博客成功',category="success")
        login_user(load_blog(blog),remember=True)

        init_blog_crawl(blog)
        return redirect(url_for('index'))

    return render_template('upload.html',form=form)


@app.route('/blog/<int:blog_id>')
def seeblog(blog_id):
    blog=Blog.query.filter_by(id=blog_id).first_or_404()
    g.menu_close="T"
    # resp.set_cookie("menu_close","T")
    return render_template('nestpage.html',title=blog.name,url=blog.homepage)

@app.route('/post/<int:post_id>')
def seepost(post_id):
    post=Post.query.filter_by(id=post_id).first_or_404()
    g.menu_close="T"
    return render_template('nestpage.html',title=post.title,url=post.url)
    

@app.route('/about/')
def about():
    return render_template('about.html')


def get_posts(page,categid,mode):

    if mode=="recommend":
        if categid==0:
            pre_process_posts=Post.query.filter(Post.recommend==True)
        else:
            pre_process_posts=Post.query.join(Blog).filter(Post.recommend==True,Blog.big_categor_id==categid)
    elif mode=="new":
        if categid==0:
            pre_process_posts=Post.query.order_by(Post.id.desc())
        else:
            pre_process_posts=Post.query.join(Blog).filter(Blog.big_categor_id==categid).order_by(Post.id.desc())
    elif mode=="random":
        if categid==0:
            pre_process_posts=Post.query.order_by(func.random())
        else:
            pre_process_posts=Post.query.join(Blog).filter(Blog.big_categor_id==categid).order_by(func.random())
    else:
        return

    pagination=pre_process_posts.paginate(
        page,app.config['POSTS_PER_NUMS'],False
    )
    return pagination



@app.route('/lookaround/<string:mode>/<int:categid>')
def lookaround(mode,categid):
    page = int(request.args.get('page',1))

    if mode=="recommend":
        pagination=get_posts(page=page,categid=categid,mode=mode)
        title="推荐文章"
    elif mode=="new":
        pagination=get_posts(page=page,categid=categid,mode=mode)
        title="最新文章"  
    elif mode=="random":
        pagination=get_posts(page=page,categid=categid,mode=mode)
        title="随机文章"
    else:
        return "mode错误"
    
    return render_template('look.html',title=title,active=categid,mode=mode,posts=pagination.items,pagination=pagination)


#处理数据
@app.route('/logos/<path:filename>')
def get_logo(filename):
    return send_from_directory(app.config['UPLOAD_LOGO_PATH'],filename)


# @app.route('/json/recommend/')
# def get_look_post():
#     page=request.args.get('page', 2, type=int)
#     posts=get_recommend_posts(page)
#     if posts:
#         return jsonify([{
#             "id":post.id,
#             "title":post.title,
#             "body":post.body,
#             "author":post.blog.name,
#             "about":post.blog.about
#         } for post in posts.items])
#     else:
#         return "end"

@app.route('/login_blog/<token>',methods=['GET','POST'])
def login_blog(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    blogid = Blog.verify_token(token)
    if not blogid:
        flash('登录错误，请联系管理员',category="error")
        return redirect(url_for('index'))
    
    #登录成功
    login_user(load_blog(blogid),remember=True)
    return redirect(url_for('backindex'))

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'),404


#后台
@app.route('/login/',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('backindex'))

    form=LoginForm()
    if form.validate_on_submit():
        blog=Blog.query.filter_by(email=form.email.data).first()
        if blog is None:
            flash('登录错误，请联系管理员',category='error')
            return redirect(url_for('index'))
        send_login_mail(blog)
        flash('邮件已发出，请通过邮件内的链接进行登录',category='success')
        flash('若未查收到邮件，请尝试翻阅垃圾箱或联系管理员',category='error')
        return redirect(url_for('index'))

    return render_template('/backsys/login_email.html',form=form)


@login_required
@app.route("/backindex/")
def backindex():
    return redirect(url_for('crawl'))

@app.route("/load/<int:id>")
def load_user_by_id(id):
    login_user(load_blog(id),remember=True)
    return redirect(url_for('crawl'))

@login_required
@app.route("/backend/postlist/")
def postlist():
    # from main.tasks import crwal_blog_data
    if current_user.crawl:
        if current_user.crawl.taskid:
            task=crwal_blog_data.AsyncResult(current_user.crawl.taskid)
            if task.successful():
                flash("爬虫任务处理完成",category="success")
                current_user.crawl.taskid=None
                task=None
            elif task.failed():
                flash("遇到未知错误，错误原因："+str(task.traceback),category="error")
                current_user.crawl.taskdone=True
                task=None
            db.session.commit()
        else:
            task=None
    else:
        task=None

    posts=Post.query.filter_by(blog=current_user).all()
    return render_template('/backsys/postlist.html',task=task,posts=posts)

@login_required
@app.route("/developing/")
def developing():
    return render_template('/backsys/developing.html')

@login_required
@app.route("/backend/crawl/",methods=['GET','POST'])
def crawl():

    #设置登录功能后对用户进行查询，获取原来的数据信息
    #如果用户已经存储，那么提交时为更新操作，参考之前的编辑用户功能

    if current_user.platform != "person":
        flash("文章爬取功能只针对个人博客用户开放")
        return redirect(url_for('postlist'))

    rform=RRSForm()
    cform=CrawlForm()

    if request.method=='GET' and current_user.crawl:
        rform.rrs_adress.data=current_user.crawl.rrs if current_user.crawl.rrs else None

        cform.post_index.data=current_user.crawl.p_home if current_user.crawl.p_home else None 
        cform.post_rule.data=current_user.crawl.p_page if current_user.crawl.p_page else None
        cform.post_titles_selector.data=current_user.crawl.p_title if current_user.crawl.p_title else None
        cform.post_links_selector.data=current_user.crawl.p_link if current_user.crawl.p_link else None
        cform.post_main_body.data=current_user.crawl.p_body if current_user.crawl.p_body else None

    isNew=False
    #此处进行判断使用原来的Crawl对象还是新建Crawl
    if current_user.crawl:
        _crawl=current_user.crawl
    else:
        isNew=True
        _crawl=Crawl

    if rform.submit1.data and rform.validate():        
        rcrawl=_crawl(rrs=rform.rrs_adress.data)
        if isNew:
            rcrawl.blog=current_user
            db.session.add(rcrawl)
            db.session.commit()
        else:
            db.session.commit()

        if not current_user.crawl.taskdone:
            flash("任务已经存在，请等待任务执行完成后再次提交更新数据")
            return redirect(url_for('postlist'))

        flash("RRS提交成功",category="success")
        #启动任务
        task=crawl_rrs_data.delay(current_user.id)
        current_user.crawl.taskid=task.id    
        current_user.crawl.taskdone=False
        db.session.commit()

        return redirect(url_for('postlist'))

    if cform.submit2.data and cform.validate():
        c_var={
            "p_home":cform.post_index.data,
            "p_page":cform.post_rule.data,
            "p_title":cform.post_titles_selector.data,
            "p_link":cform.post_links_selector.data,
            "p_body":cform.post_main_body.data
        }
        ccrawl=_crawl(**c_var)
        if isNew:
            ccrawl.blog=current_user
            db.session.add(ccrawl)
            db.session.commit()
        else:
            db.session.commit()
        

        if not current_user.crawl.taskdone:
            flash("任务已经存在，请等待任务执行完成后再次提交更新数据")
            return redirect(url_for('postlist'))

        #启动任务
        task=crwal_blog_data.delay(current_user.id,True)
        current_user.crawl.taskid=task.id    
        current_user.crawl.taskdone=False
        db.session.commit()
        return redirect(url_for('postlist'))

    return render_template('/backsys/crawl.html',rform=rform,cform=cform)

    
    