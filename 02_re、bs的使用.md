# 02 re、bs的使用

re和beautifulsoup都是处理超文本非常好用的工具，可以非常方便地从文本中获得自己需要的信息。

## 1 beautifulsoup

beautifulsoup非常好用且方便，即便你不是很懂正则表达式，也可以轻松的解析返回的请求。

主要需要掌握的用法有以下几点

* 引用

```python
from bs4 import BeautifulSoup
```

* 解析

```python
soup = BeautifulSoup(html, 'lxml')#解析器有python自带的html.parser\lxml\xml\html5lib 这里使用lxml
```

* 查找

```python
soup.find_all('ul') #查找所有ul,返回list
soup.find_all(attrs={'id': 'list'}) # 按照属性查找
soup.find_all(text='abc') # 按照文本内容查找
soup.find('ul')  #查找第一个出现ul
```

* 获取

```python
# 获取p标签下的id属性值，两种方式
soup.p.attrs['id']
soup.p['id']
# 获取文本
soup.get_text()
```

第一节中根据返回的html，手动截取的这一段的文本，通过beautifulsoup，可以直接找出来这一段信息。

```html
 <tr class="odd"><td><a href="/film/6923" title="唐人街探案2">唐人街探案2</a></td><td>7.5万</td><td>186.53万</td><td>6831.12万</td><td>23.61亿</td> </tr>
 <tr class="even"><td><a href="/film/7276" title="红海行动">红海行动</a></td><td>7.21万</td><td>238.62万</td><td>9346.27万</td><td>17.27亿</td> </tr>
 <tr class="odd"><td><a href="/film/6563" title="捉妖记2">捉妖记2</a></td><td>4.27万</td><td>72.42万</td><td>2598.82万</td><td>18.94亿</td> </tr>
```

代码如下

```python
from urllib import request # 引用urllib中的request
from bs4 import BeautifulSoup
if __name__ == "__main__":
    response = request.urlopen("http://58921.com") #获取网址请求返回值
    html =str(response.read(), encoding='utf-8') # 返回bytes转为utf8
    soup = BeautifulSoup(html, 'lxml')
    print(soup.find_all(attrs={'id': 'front_block_top_day'}))
```

结果如下

```html
<div class="tab-pane active" id="front_block_top_day"><div class="table-responsive"><table class="center_table table table-bordered table-condensed">
<thead><tr><th>电影名称</th><th>昨日票房</th><th>累积</th></tr></thead><tbody>
<tr class="odd"><td class="left"><a href="/film/7276" title="红海行动">红海行动</a></td><td data-toggle="tooltip" title="更新时间：2018/02/24 23:58:02">2.25亿</td><td>20.87亿</td> </tr>
<tr class="even"><td class="left"><a href="/film/6923" title="唐人街探案2">唐人街探案2</a></td><td data-toggle="tooltip" title="更新时间：2018/02/24 23:58:02">1.71亿</td><td>26.12亿</td> </tr>
<tr class="odd"><td class="left"><a href="/film/6563" title="捉妖记2">捉妖记2</a></td><td data-toggle="tooltip" title="更新时间：2018/02/24 23:58:02">6773.54万</td><td>19.98亿</td> </tr>
<tr class="even"><td class="left"><a href="/film/7338" title="熊出没之变形记">熊出没之变形记</a></td><td data-toggle="tooltip" title="更新时间：2018/02/24 23:58:02">2481万</td><td>5.28亿</td> </tr>
<tr class="odd"><td class="left"><a href="/film/7570" title="西游记女儿国">西游记女儿国</a></td><td data-toggle="tooltip" title="更新时间：2018/02/24 23:58:02">1446.67万</td><td>6.72亿</td> </tr>
</tbody>
</table>
</div></div>
```

这样可以大概定位我要找的信息,在findall的基础上，在加一个find

```python
soup.find_all(attrs={'id': 'front_block_top_day'})[0].find('tbody')
```

下一步，按照tr再次findall，得到每一个电影的信息，为list中的一个元素，然后获得电影名属性值，print出来

```python
all=soup.find_all(attrs={'id': 'front_block_top_day'})[0].find('tbody').find_all('tr')
for film in all:
    print(film.a.attrs['title'])
```

结果如下

```text
红海行动
唐人街探案2
捉妖记2
熊出没之变形记
西游记女儿国
```

由于票房数据是text，不能用获取属性的方式获取，因此，采用get_text()获取

```python
for film in all:
    args = film.find_all('td')
    print(args[0].get_text(),args[1].get_text(),args[2].get_text())
```

得到结果如下

```text
红海行动 2.25亿 20.93亿
唐人街探案2 1.71亿 26.16亿
捉妖记2 6773.54万 19.99亿
熊出没之变形记 2481万 5.28亿
西游记女儿国 1446.67万 6.72亿
```

爬虫的工作接近尾声了，但还有一个问题，票房数据不规整，并不是数字，而且单位有万有亿，这就需要re上场了

## 2 re

re(regular expression)正则表达式，re功能非常强大，这里先简单介绍一下最常用的几种

```python
re.findall('\d+',string)#找出所有整数
re.findall('\d+\.?\d+',string)#找出所有数字，带小数
re.findall('\D+',string)#找出所有非数字
```

对于现有的票房数据，我们可以看到，是有小数的，且单位在每个字符串的最后，所以，可以按下面的方式获取数据

```python
for film in all:
    args = film.find_all('td')
    print(args[0].get_text(),
    re.findall(r'\d+\.?\d+',args[1].get_text())[0],
    re.findall(r'\D',args[1].get_text())[-1],
    re.findall(r'\d+\.?\d+',args[2].get_text())[0],
    re.findall(r'\D',args[2].get_text())[-1])
```

结果如下

```text
红海行动 2.25 亿 2.25 亿
唐人街探案2 1.71 亿 1.71 亿
捉妖记2 6773.54 万 6773.54 万
熊出没之变形记 2481 万 2481 万
西游记女儿国 1446.67 万 1446.67 万
```

至此，爬虫的工作基本上算是完成了。

## 总结

一句话，尽量用beautifulsoup对文本解析，实在有搞不定的再用re,这样的效率可以最高。