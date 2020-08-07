from flask_script import Shell
from main.start import app,db,manager
from main.models import BigCategor,Blog

#shell注册
def make_shell_context():
    return dict(app=app,db=db,Blog=Blog,BigCategor=BigCategor)

manager.add_command("shell",Shell(make_context=make_shell_context))