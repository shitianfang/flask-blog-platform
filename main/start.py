from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager
from flask_avatars import Avatars
from flask_cli import FlaskCLI
from flask_login import LoginManager
from flask_mail import Mail
from celery import Celery


#初始化
app=Flask(__name__)
app.config.from_object('main.config')
db=SQLAlchemy(app)
migrate=Migrate(app,db,render_as_batch=True)
manager=Manager(app)
avatars=Avatars(app)
cli=FlaskCLI(app)
login=LoginManager(app)
mail=Mail(app)


#模块配置
login.login_view='login'
celery=Celery(app.import_name, backend="redis://127.0.0.1:6379/0", broker="redis://127.0.0.1:6379/0")
celery.conf.update(app.config)

#个人设置
app.jinja_env.auto_reload=True


#监听文件
import main.models
import main.views
import main.tasks

#注册函数与数据
import main.shell_manage
import main.tools.make_fake_data


    