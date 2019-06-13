import requests
from bs4 import BeautifulSoup
import json


s = requests.session()
headers = {
    'cookie':'t=e09b62ffc2546a8b2ab8e5e28ad8a119; cna=z6IxFY4JJ08CAdpsHWv+rPAc; miid=1257104789759174727; cookie2=3b22d6c2515bfbd321dda6bd7145e068; v=0; _tb_token_=e375337058536; thw=cn; tracknick=wxyhhh6; lgc=wxyhhh6; dnk=wxyhhh6; tg=0; unb=2787601707; sg=67c; _l_g_=Ug%3D%3D; skt=53ec3eccff9dd322; cookie1=B0Sthht%2Fyd909A7hKBFlJWLZfyQojNM2sPQLhDfWlmc%3D; csg=cd7cb538; uc3=vt3=F8dBy3ke1KIpRXsrQ%2FU%3D&id2=UU8A4THY92uLQg%3D%3D&nk2=FOGMYC3MeA%3D%3D&lg2=UtASsssmOIJ0bQ%3D%3D; existShop=MTU2MDQxMTM0Mw%3D%3D; _cc_=VFC%2FuZ9ajQ%3D%3D; _nk_=wxyhhh6; cookie17=UU8A4THY92uLQg%3D%3D; enc=9TzTWC%2F%2F1n4ItMlk9ZS4BjPM73rPG%2FtAer%2F2%2Fv2RG9I833DX1n2iHIoG8A2VDAaTM%2FjvRqnu9zoCCz9uMVWvsA%3D%3D; mt=ci=6_1; uc1="cookie15=VT5L2FSpMGV7TQ%3D%3D"; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=218545; JSESSIONID=E099EBAFF34CBEA7AE2D2E774EFB43B9; l=bBET3docvnaTK47CBOCiIZMuwEbtOIRAguWXraDei_5pQ6YsEP_OkjTQhFv6Vj5RsvYB4-L8Y1J9-etki; isg=BBYWvwzMV-Agt2Lpl1BFfHZ3Z8wSYZqngV_DPIB_JPmUQ7bd6EVNAMsx358Ka1IJ',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
r = s.get("https://s.taobao.com/search?q=%E6%B4%97%E8%A1%A3%E6%B6%B2", headers=headers)

soup = BeautifulSoup(r.text, 'html.parser')

jsonStr = soup.select("head > script")[-1].text.strip().split('\n')[0].split('=')[1]

jsonStr = jsonStr.rstrip(';').strip()

jsonObj = json.loads(jsonStr)
pic_url = jsonObj['mods']['itemlist']['data']['auctions'][0]['pic_url'] + '_260x260.jpg'

r = s.get('https:' + pic_url)
with open('images/'+ pic_url.split('/')[-1], 'wb+') as f:
    f.write(r.content)


print(pic_url)
