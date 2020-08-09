# flask-blog-platform

项目自带爬虫功能，可以爬取博客文章

# 使用方法：
运行run.py文件

若需要爬取文章，则需要启动celery
celery -A main.start.celery worker -l info -P eventlet 
或
celery -A main.start.celery worker -l info --pool=solo

在Linux后台运行可以使用：
supervisord -c /目录/supervisord.conf


#有问题可以加QQ群交流：1126037372

感谢Viggo前端 https://github.com/WebStackPage/WebStackPage.github.io

# 效果
![](https://github.com/shitianfang/flask-blog-platform/blob/master/a.png)
![](https://github.com/shitianfang/flask-blog-platform/blob/master/b.png)
