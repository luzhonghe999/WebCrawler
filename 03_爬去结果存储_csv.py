from urllib import request # 引用urllib中的request
from bs4 import BeautifulSoup
import re
import pandas as pd
from pandas import DataFrame
if __name__ == "__main__":
    response = request.urlopen("http://58921.com") #获取网址请求返回值
    html =str(response.read(), encoding='utf-8') # 返回bytes转为utf8
    soup = BeautifulSoup(html, 'lxml')
    all=soup.find_all(attrs={'id': 'front_block_top_day'})[0].find('tbody').find_all('tr')
    # for film in all:
    #     print(film.a.attrs['title'])
    all_film=[]
    for film in all:
        args = film.find_all('td')
        film_info=[args[0].get_text(), 
        re.findall(r'\d+\.?\d+',args[1].get_text())[0], 
        re.findall(r'\D',args[1].get_text())[-1],
        re.findall(r'\d+\.?\d+',args[2].get_text())[0],
        re.findall(r'\D',args[2].get_text())[-1]]
        all_film.append(film_info)
    df=DataFrame(all_film)
    df.columns = ['film_name', 'y_box_office', 'unit1', 'a_box_office', 'unit2']
    df.to_csv("d:/test.csv",index=False)