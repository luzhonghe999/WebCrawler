from urllib import request # 引用urllib中的request
if __name__ == "__main__":
    response = request.urlopen("http://58921.com") #获取网址请求返回值
    html =str(response.read(), encoding='utf-8') # 返回bytes转为utf8
    print(html)