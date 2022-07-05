from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import re
import json



headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    }#你的身分
r2=requests.get('https://forum.gamer.com.tw/B.php?bsn=7650', headers=headers) #getmethod 查詢搜尋
html2= r2.content.decode("utf-8") #byte轉str
sp2=BeautifulSoup(html2,'html.parser') #bs解析html原始碼
#a="["
d_list=[]
for index,link in enumerate(sp2.find_all("p", href=True)):
        if(index<14):
            myurl="https://forum.gamer.com.tw/"+link['href']
            add={'title':link.text,'url':myurl}
            d_list.append(add)

with open("static/data/input.json", 'w',encoding='UTF-8' ) as file:
        json.dump(d_list, file)
file.close()