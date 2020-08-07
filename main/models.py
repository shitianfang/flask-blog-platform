from main.start import db,app,login
from flask_login import UserMixin
from time import time
import jwt




#此处需要新建一张分类表，然后建立外键关联
#还需要建立一个评分表，空闲时计算评分，数字字段范围设置
#建立一个标签表，也是新建一张标签表，建立外键关联


class BigCategor(db.Model):
    __tablename__="bigcategors"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),nullable=False,unique=True)
    hot=db.Column(db.Boolean)
    icon=db.Column(db.String(20))

    #注意可以默认通过关系属性访问一个列表，但如果定义lazy为dynamic，则返回查询对象
    blogs=db.relationship('Blog',backref='big_categor',lazy='dynamic') 



#当前一个博客大约占用0.7kb的空间
class Blog(UserMixin,db.Model):
    __tablename__="blogs"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),index=True,unique=True,nullable=False)
    email=db.Column(db.String(120),index=True,unique=True,nullable=True)
    homepage=db.Column(db.String(255),unique=True,nullable=False)
    about=db.Column(db.String(280))
    last_update=db.Column(db.DateTime)
    logo=db.Column(db.String(80))
    keyword=db.Column(db.String(64))
    platform=db.Column(db.String(20))
    # login_token=db.Column(db.String(128))

    #外键，注意外键参数内前面是表名
    big_categor_id=db.Column(db.Integer,db.ForeignKey('bigcategors.id'))

    #关系
    posts=db.relationship('Post',backref='blog',lazy='dynamic') 
    crawl=db.relationship('Crawl',backref='blog',uselist=False)

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['login_token']
        except:
            return

        return id

    def get_token(self,expires_in=86400):
        return jwt.encode(
            {
                'login_token':self.id,
                'exp':time()+expires_in
            },
            app.config['SECRET_KEY'],algorithm='HS256'
        ).decode('utf-8')

    

class Post(db.Model):
    __tablename__="posts"

    id=db.Column(db.Integer,primary_key=True)
    url=db.Column(db.String(255))
    title=db.Column(db.String(125))
    body=db.Column(db.Text)
    digest=db.Column(db.String(300))
    recommend=db.Column(db.Boolean,default=False)
    # md5=db.Column(db.String(32))
    blog_id=db.Column(db.Integer,db.ForeignKey('blogs.id'))
    
    
    #hashlib.md5(url).hexdigest()

class Crawl(db.Model):
    __tablename__="crawls"

    id=db.Column(db.Integer,primary_key=True)
    rrs=db.Column(db.String(255))
    p_home=db.Column(db.String(255))
    p_page=db.Column(db.String(225))
    p_title=db.Column(db.String(125))
    p_link=db.Column(db.String(125))
    p_body=db.Column(db.String(125))
    taskid=db.Column(db.String(125))
    taskdone=db.Column(db.Boolean,default=True)
    urlset=db.Column(db.Text)

    # tasks = db.relationship('Task', backref='crawl', lazy='dynamic')
    
    blog_id=db.Column(db.Integer,db.ForeignKey('blogs.id'))

    def __call__(self, *args, **kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)
        # return super().__call__(*args, **kwargs)


    def get(self,attr):
        return getattr(self,attr)



            


@login.user_loader
def load_blog(id_or_blog):
    if isinstance(id_or_blog,str):
        return Blog.query.get(int(id_or_blog))
    elif isinstance(id_or_blog,int):
        return Blog.query.get(id_or_blog)
    else:
        return id_or_blog

    



