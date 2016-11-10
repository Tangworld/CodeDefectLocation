import requests


newsurl = 'https://news.sina.com.cn/'
res = requests.get( newsurl )
res.encoding = 'utf-8'
print (res.content)
