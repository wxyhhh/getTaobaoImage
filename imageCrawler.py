#! /usr/bin/env python
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import json
import pymysql
import time

def dealCheck(browser):
    js1 = '''Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) '''
    js2 = '''window.navigator.chrome = { runtime: {},  }; '''
    js3 = '''Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); '''
    js4 = '''Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); '''
    browser.execute_script(js1)
    browser.execute_script(js2)
    browser.execute_script(js3)
    browser.execute_script(js4)
    time.sleep(1)
    while True:
        buttons = browser.find_elements_by_id('nc_1_n1z')
        if len(buttons) > 0:
            print("no!")
            action = ActionChains(browser)
            action.click_and_hold(buttons[0]).perform()
            action.reset_actions()
            action.move_by_offset(320, 0).perform()
            time.sleep(3)
            js1 = '''Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) '''
            js2 = '''window.navigator.chrome = { runtime: {},  }; '''
            js3 = '''Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); '''
            js4 = '''Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); '''
            browser.execute_script(js1)
            browser.execute_script(js2)
            browser.execute_script(js3)
            browser.execute_script(js4)
        else:
            break

db = pymysql.connect("rm-bp1wlg5jh7jb42c29o.mysql.rds.aliyuncs.com", "quality", "quality@302", "quality-site-19", charset='utf8')
cursor = db.cursor()

proxies = {"https":"163.204.241.238:9999"}

s = requests.session()
cookie_str = 'miid=5437891741066503936; t=9a3bd850418114edf851e7f294474c38; cna=L6h5Ei8dtnACAXrh3I1vvfwJ; tracknick=wxyhhh6; tg=0; thw=cn; enc=YPMxoac8fT%2BqN2P4AymgskoTr%2FBzPROOUnfOhNAn7QGDkgLam4BfkrriWfVaLM7LUok9ayhIbKgEvhvO7GFPog%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; lgc=wxyhhh6; UM_distinctid=16a9d39a67c872-0264390706479d-b781636-144000-16a9d39a67d397; uc3=vt3=F8dBy3qM2Cue8HqrPo0%3D&id2=UU8A4THY92uLQg%3D%3D&nk2=FOGMYC3MeA%3D%3D&lg2=URm48syIIVrSKA%3D%3D; _cc_=VT5L2FSpdA%3D%3D; mt=ci=-1_0; _m_h5_tk=c35965814df7fcdb67bc1cae69e2332e_1560239629863; _m_h5_tk_enc=635b00bfde4cf564c90a53b79d1acce3; v=0; cookie2=1131ca87dde19fcd06315c37f4c1fbe9; _tb_token_=759ae358ee3fd; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; swfstore=267363; _uab_collina=156044605736896918535159; JSESSIONID=6D09DD3E1E59C87002EC6E7896978D6D; uc1=cookie14=UoTaGOxeWIrhHA%3D%3D; isg=BDIyZZ7_u08CO4BAYBvyqZxCg3jG46dllNb9bvwLJ-XQj9CJ5FOGbTi5eysz-a71; l=bBrbeSzrvPf8ohnwBOCaCUqXdjQTMIR4ouJuGIupi_5gr1T1na7OkjWOGe96Vj5RsfLB4s6vWje9-etln'
headers = {
    'cookie':cookie_str,
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

# options = Options()
# options.set_headless()
browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
browser.delete_all_cookies()
browser.get('https://s.taobao.com/search?q=%E6%9E%B8%E6%9D%9E%E7%BA%A2%E7%B3%96+%E4%B8%8A%E7%8F%8D%E6%9E%9C')
cookielist = []
for item in cookie_str.split('; '):
    cookie = {}
    itemname = item.split('=')[0]
    iremvalue = item.lstrip(itemname).lstrip('=')
    cookie['name'] = itemname
    cookie['value'] = iremvalue
    cookie['domain'] = ".taobao.com"
    cookie['path'] = "/"
    cookie['expires'] = ""
    if not browser.get_cookie(itemname):
        browser.add_cookie(cookie)

browser.refresh()


sql = "select id, name, specification, brand from product where img like '%categories%'"
cursor.execute(sql)
results = cursor.fetchall()
id = results[0][0]
try:
    for result in results:
        id = result[0]
        name = result[1]
        specification = ''
        if result[2] != '/':
            specification = result[2].split('/')[0]
        brand = ''
        if result[3] != '/':
            brand = result[3]
        url = "https://s.taobao.com/search?q=" + name + "+" + specification + "+" + brand
        # r = s.get(url, headers=headers)
        browser.get(url)
        dealCheck(browser)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        scripts = soup.select("head > script")
        jsonStr = ''
        for script in scripts:
            if script.text.strip() != '' and script.text.strip()[0] == 'g':
                jsonStr = script.text.strip().split('\n')[0].split('=')[1]
                break

        jsonStr = jsonStr.rstrip(';').strip()

        jsonObj = json.loads(jsonStr)
        if not 'data' in jsonObj['mods']['itemlist']:
            continue
            # browser.refresh()
            # dealCheck(browser)
            #
            # soup = BeautifulSoup(browser.page_source, 'html.parser')
            # scripts = soup.select("head > script")
            # jsonStr = ''
            # for script in scripts:
            #     if script.text.strip() != '' and script.text.strip()[0] == 'g':
            #         jsonStr = script.text.strip().split('\n')[0].split('=')[1]
            #         break
            # jsonStr = jsonStr.rstrip(';').strip()
            # jsonObj = json.loads(jsonStr)

        pic_url = jsonObj['mods']['itemlist']['data']['auctions'][0]['pic_url'] + '_260x260.jpg'

        print(pic_url)
        r = s.get('https:' + pic_url)
        with open('/home/deploy/quality-19/uploadFiles/products/' + pic_url.split('/')[-1], 'wb+') as f:
            f.write(r.content)
        img = "/products/images/" + pic_url.split('/')[-1]
        sql = "update product set img = '%s' where id = '%s'" % (img, id)
        cursor.execute(sql)
        db.commit()

    browser.quit()

except Exception as e:
    print(e.with_traceback())
    db.rollback()
    print(id)
    browser.quit()
