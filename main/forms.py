from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SubmitField,IntegerField,RadioField
from wtforms.validators import Length,DataRequired,URL,AnyOf,Email,ValidationError
from flask_wtf.file import FileField,FileAllowed,FileRequired
from main.cache import categors
from main.models import Blog

class Email_nullable(Email):
    def __call__(self, form, field):
        value = field.data

        message = self.message
        if message is None:
            message = field.gettext('Invalid email address.')      

        if value:

            if '@' not in value:
                raise ValidationError(message)

            user_part, domain_part = value.rsplit('@', 1)

            if not self.user_regex.match(user_part):
                raise ValidationError(message)

            if not self.validate_hostname(domain_part):
                raise ValidationError(message)

class BlogForm(FlaskForm):
    logo=FileField("LOGO*",validators=[FileRequired(),FileAllowed(['jpg','jpeg','png','gif','bmp'])])
    name=StringField('博客名称*',validators=[DataRequired(),Length(min=0,max=64)])
    url=StringField('博客主页*',validators=[DataRequired(),URL(),Length(min=0,max=255)])
    email=StringField('登录邮箱*',validators=[Email(),Length(min=0,max=120)])
    # about=StringField('博客简介（限140中文字）',validators=[Length(min=0,max=280)])
    # keyword=StringField('关键词（用逗号分隔，中英文都可以）',validators=[Length(min=0,max=64)])
    categor=SelectField("选择主分类*",validators=[DataRequired()],choices=[(c.id,c.name) for c in categors],coerce=int,default=2) 
    platform=RadioField("博客平台",choices=[('person','个人博客'),('csdn','CSDN'),('cnblogs','博客园')],default='person') #('jianshu','简书')
    submit=SubmitField('提交博客')

    def validate_name(self,name):
        blog=Blog.query.filter_by(name=name.data).first()
        if blog is not None:
            raise ValidationError('博客名已存在')   
    
    def validate_url(self,url):
        if self.platform.data=="csdn":
            if url.data[8:10]!="me" and url.data[8:12]!="blog":
                raise ValidationError("请输入正确的个人主页链接或重新选择博客平台")
        
        if self.platform.data=="cnblogs":
            if url.data[12:19]!="cnblogs":
                raise ValidationError("请输入正确的个人主页链接或重新选择博客平台")
    
class RRSForm(FlaskForm):
    rrs_adress=StringField('RRS地址',validators=[URL(),Length(min=0,max=128)])
    submit1=SubmitField('提交SSR地址')

    
class CrawlForm(FlaskForm):
    post_index=StringField('文章列表主页地址',validators=[URL(),Length(min=0,max=128)])
    post_rule=StringField('文章列表分页规则',validators=[Length(min=0,max=128)])
    # post_second_num=IntegerField("列表分页第二页<num>处数字")
    post_titles_selector=StringField('文章列表标题选择器',validators=[DataRequired(),Length(min=0,max=128)])
    post_links_selector=StringField('文章列表链接选择器',validators=[DataRequired(),Length(min=0,max=128)])
    post_main_body=StringField('文章页面正文选择器',validators=[DataRequired(),Length(min=0,max=128)])
    submit2=SubmitField('提交爬虫规则')

    def validate_post_rule(self,rule):
        if rule.data:
            if "<num>" not in rule.data:
                raise ValidationError("<num>不在列表分页规则中，若无分页请留空字段")

class LoginForm(FlaskForm):
    email=StringField('邮箱',validators=[Email()])

    def validate_email(self,email):
        blog=Blog.query.filter_by(email=email.data).first()
        if blog is None:
            raise ValidationError('邮箱不存在')