import re
from bs4 import BeautifulSoup
import requests
import time

sever = 'http://xiaohua.zol.com.cn/'
list = 'http://xiaohua.zol.com.cn/new/'
new = 'http://xiaohua.zol.com.cn/new/'
num = 0
# 　　  # 设置头信息
# headers_base = {
#     'host': 'xiaohua.zol.com.cn',
#     'Connection': 'keep-alive',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
#     'Referer': 'http://xiaohua.zol.com.cn/',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9'
# }
# headers_base = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
# }
headers_base = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'ip_ck=7sOJ5/L2j7QuOTQ4MDgxLjE1ODE5NDc1NDA%3D; lv=1589804913; vn=2; Hm_lvt_ae5edc2bc4fc71370807f6187f0a2dd0=1589804914; _ga=GA1.3.1811789677.1589804914; _gid=GA1.3.506634774.1589804914; bdshare_firstime=1589804913989; Hm_lpvt_ae5edc2bc4fc71370807f6187f0a2dd0=1589810331; _gat=1; questionnaire_pv=1589760025; dc4c9bf699eda6bca78b2c42efbd920e=13i2abo2g2g39j30m2a2n%7B%7BZ%7D%7D5%7B%7BZ%7D%7Dnull; 93f3d4f8e19ffac58e54d318a37efe74=13i2abo2g2g39j30m2a2n%7B%7BZ%7D%7D5%7B%7BZ%7D%7Dnull; MyZClick_dc4c9bf699eda6bca78b2c42efbd920e=/html/body/div%5B6%5D/div/div%5B2%5D/div/a%5B4%5D/; MyZClick_93f3d4f8e19ffac58e54d318a37efe74=/html/body/div%5B6%5D/div/div%5B2%5D/div/a%5B4%5D/',
    'Host': 'xiaohua.zol.com.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://xiaohua.zol.com.cn/new/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }

for i in range(2, 200):
    list_link = new + str(i) + '.html'
    print(list_link)
    # try:
    req = requests.get(list_link, headers=headers_base)
    # except:
    #     break

    html = req.text
    soup = BeautifulSoup(html, "lxml")
    result = soup.find_all('li', class_='article-summary')
    if not result:
        print('66666666666666666666666666666666666666666')
        print(html)
        print('66666666666666666666666666666666666666666')
    # else:
    #     print('11111111111111111111111111111111111111111111')
    #     print(result)
    #     print('11111111111111111111111111111111111111111111')

    for i in result:
        all_read_link = sever + i.find(class_='all-read').get('href')
        print(all_read_link)
        # try:
        all_read_html = requests.get(all_read_link).text
        # except:
        #     break
        soup = BeautifulSoup(all_read_html, "lxml")
        article_list = soup.find_all(class_='article-text')
        for i in article_list:
            article = i.text
            article = re.sub('[0-9].*|[0-9]、|————| * |\n|	', '\n', article)
            # print(article)
            with open('../笑话2.txt', 'at') as f:
                f.writelines(article)
            num = num + 1
            print('完成:{}段'.format(num))
            # time.sleep(1000000000)