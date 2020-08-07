from main.models import BigCategor

class categor:
    def __init__(self,id,name,hot,icon):
        self.id=id
        self.name=name
        self.hot=hot
        self.icon=icon

#注意此处可能引起无法正常启动，必要时注释或解决
try:
    datas=BigCategor.query.all()
    categors=[]
    for c in datas:
        categors.append(categor(c.id,c.name,c.hot,c.icon))
except:
    categors=[]
    print("未正确查找到侧边导航项目")
