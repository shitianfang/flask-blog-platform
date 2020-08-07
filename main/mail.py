from main.start import app,mail
from flask_mail import Message
from flask import render_template
from threading import Thread


#附件发送方法
#attachments=[('posts.json', 'application/json',json.dumps({'posts': data}, indent=4))]



#recipients为列表
def send_mail(subject,text_body=None,html_body=None,sender=None,recipients=None,attachments=None,sync=False):
    sender=app.config["MAIL_DEFAULT_SENDER"]
    title=app.config["FLASKY_MAIL_SUBJECT_PREFIX"]+" "+subject
    msg=Message(title,sender=sender,recipients=recipients)
    msg.body=text_body
    msg.html=html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    
    if sync:
        mail.send(msg)
    else:
        #线程发送邮件 
        Thread(target=send_async_email,args=(app,msg)).start()
    
    
def send_login_mail(blog):
    token=blog.get_token()
    send_mail('登录您的账户',recipients=[blog.email],
        text_body=render_template('mail/login_blog.txt',
            blog=blog,token=token),
        html_body=render_template('mail/login_blog.html',
            blog=blog,token=token))


def send_crawl_mail(blog):
    send_mail('您的文章已更新完毕',recipients=[blog.email],
        text_body=render_template('mail/crawl_complete.txt',
            blog=blog),
        html_body=render_template('mail/crawl_complete.html',
            blog=blog))


   
def send_async_email(app,msg):
    #开启app上下文
    with app.app_context():
        #因为send方法需要访问app配置
        mail.send(msg)


