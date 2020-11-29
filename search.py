#!/usr/bin/python
#@Author: zhongshsh

# 不能爬取表格
# 如果报错list超出范围，可能是网页无目录

import requests
import re
from bs4 import BeautifulSoup, NavigableString
import urllib

def get_html(url):
        headers = {
        'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
        AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        return response.text

# 删除超链接,保留标签内的内容
def strip_tags(html, invalid_tags):
    soup = BeautifulSoup(html, 'lxml')
    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""
            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(str(c), invalid_tags)
                s += str(c)
            tag.replaceWith(s)
    return soup

# 删除标引
def strip_by(soup):
    [s.extract() for s in soup('sup')]
    [s.extract() for s in soup('sub')]
    return soup

# 获取列表信息
def get_ls(html):
    pattern = re.compile('class=\"basicInfo-block basicInfo-left\">(.*?)</dl>.*?'
                         'class=\"basicInfo-block basicInfo-right\">(.*?)</dl>', re.S)
    pa = re.findall(pattern, html)
    soup = BeautifulSoup(str(strip_tags(str(pa[0]), ['a','br'])).replace('\\n',''),'lxml')
    dt_list=[]
    dd_list=[]
    for i in soup.find_all('dt'):
        dt_list.append(i.string)
    for i in soup.find_all('dd'):
        dd_list.append(i.string)
    return dt_list,dd_list

# 爬取目录
def ml(html):
    pattern = re.compile('class=\"catalog-list.*?>(.*?)</div>', re.S)
    pa = re.findall(pattern, html)
    soup = BeautifulSoup(str(pa[0]), 'lxml')
    ml_list=[]
    for i in soup.find_all('a'):
        ml_list.append(i.string)
    return ml_list

# 爬取内容
def cont(html):
    cont_list = html.split('title-text')
    ct = []
    for i in range(len(cont_list)):
        if i == 0:
            continue
        else:
            soup = strip_by(strip_tags(cont_list[i], ['a','i','b']))
            soup = BeautifulSoup(str(soup).replace('\n',''),'lxml')
            string=''
            for i in soup.find_all(attrs={'label-module':"para"}):
                if i.string != None and i.string.find('img') == -1:
                    string=string+i.string.replace('<html><body>','').replace('</body></html>','')+'\n'  # 需要改进一下去除标签部分
            ct.append(string)
    return ct

def search(item):
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(item)
    html = get_html(url)

    pattern = re.compile('promotion-declaration.*?</div>(.*?)'
                         '<div class=\"lemmaWgt-promotion-leadPVBtn\"', re.S)
    pa = re.findall(pattern, html)
    html_pa = ''
    for i in pa:
        html_pa = i
    return (strip_by(strip_tags(html_pa.replace('\n', ''), ['a'])).text)  # 获取简介



