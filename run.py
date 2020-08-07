import sys,os

sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+"/main")
# print("路径：",sys.path)
from main.start import app

app=app

if __name__=="__main__":
    app.run(debug=True)