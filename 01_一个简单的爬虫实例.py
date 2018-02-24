from urllib import request
if __name__ == "__main__":
    response = request.urlopen("http://58921.com")
    html =str(response.read(), encoding='utf-8') 
    print(html)