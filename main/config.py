import os
from datetime import timedelta
basedir=os.path.abspath(os.path.dirname(__file__))


#只有大写命名会被加载到配置中
SECRET_KEY=os.environ.get('SECRET_KEY') or 'biu,biu,biu'
FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')

#数据库配置
SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,"data",'blog_collect.db?check_same_thread=False')#
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_LOGO_PATH=os.path.join(basedir,'data','logo')

#激活跨站点请求伪造保护，激活更安全
CSRF_ENABLED=True 

#每行显示博客卡片个数
BLOGS_PER_ROW=4

#每类最多显示博客个数
BLOGS_PER_CATE=40

#每次Ajax加载帖子数量
POSTS_PER_NUMS=10

#最大上传文件大小
MAX_CONTENT_LENGTH=3*1024*1024

#自动刷新模板
TEMPLATES_AUTO_RELOAD = True


#邮件配置
MAIL_DEBUG = True             # 开启debug，便于调试看信息
MAIL_SUPPRESS_SEND = False    # 发送邮件，为True则不发送
MAIL_SERVER = 'smtp.qq.com'   # 邮箱服务器
MAIL_PORT = 465               # 端口
MAIL_USE_SSL = True           # 重要，qq邮箱需要使用SSL
MAIL_USE_TLS = False          # 不需要使用TLS
MAIL_USERNAME = 'admin@qq.com'  # 填邮箱
MAIL_PASSWORD = ''        # 填授权码
MAIL_DEFAULT_SENDER= 'admin@qq.com' #默认发送人
FLASKY_MAIL_SUBJECT_PREFIX = '[MyBlog团队]' #标题前缀
ADMINS = ['admin@qq.com'] #管理员


#Redis-Celery配置
CELERY_BROKER_URL="redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/0"
CELERYD_PREFETCH_MULTIPLIER = 2 #每次取的任务工作数量
CELERY_TASK_RESULT_EXPIRES = 600 #超时时间10分钟
CELERYD_CONCURRENCY = 2 #并发Workder数


