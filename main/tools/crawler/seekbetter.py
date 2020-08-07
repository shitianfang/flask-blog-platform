from pyquery import PyQuery as pq
import requests

url="https://seekbetter.me/?sort=recommend&mode=blog&page=<num>"
# print(requests.get("https://seekbetter.me/forward/blog/81",verify=False).url)

f=open("seekbetter.txt","w",encoding='UTF-8')

# requests.packages.urllib3.disable_warnings()

try:
    for i in range(1,11):
        url_page=url.replace("<num>",str(i))
        print(url_page)
        doc=pq(requests.get(url_page,verify=False).text)
        cards=doc(".cards-item").items()

        for card in cards:        
            name=card(".blog_name").text()
            desc=card(".blog_desc").text()
            tag=card(".mb-2").text()
            resp=requests.get("https://seekbetter.me"+card(".d-block").attr.href,verify=False)
            print(resp.status_code)
            url=resp.url
            text="名称："+name+"\n"+"描述："+desc+"\n"+"标签："+tag+"\n"+"链接："+url+"\n\n\n"
            print(text)
            f.write(text)
except BaseException as e:
    print(repr(e))
finally:
    print("完成")
    f.close()








