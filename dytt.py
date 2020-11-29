import requests
from lxml import etree
import json
import random

BASE_DIMAIN = "http://www.dytt8.net"  # 定义基础域名
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}


# 获取电影列表页的链接
def movie_list_page():
    base_url = "http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"
    page_urls = []
    for x in range(1, 2):
        page_urls.append(base_url.format(x))

    return page_urls


# 传入电影列表页地址，返回这一页中每一部电影的详情页面链接
def get_detail_url(url):
    response = requests.get(url, headers=HEADERS)
    text = response.text
    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a[@href!='/html/gndy/jddy/index.html']/@href")
    detail_urls = map(lambda x: BASE_DIMAIN + x, detail_urls)

    return detail_urls


# 通过电影的详情页面链接，获取电影的全部数据
def get_movie_content(url):
    movie = {}
    detail_response = requests.get(url, headers=HEADERS)
    detail_text = detail_response.content.decode(encoding="gb18030", errors="ignore")
    detail_html = etree.HTML(detail_text)

    if len(detail_html.xpath("//div[@id='Zoom']")) > 0:
        zoom = detail_html.xpath("//div[@id='Zoom']")[0]
    else:
        return movie            # 说明没有爬取成功，直接跳过返回一个空字典

    # text_list = zoom.xpath(".//p/text()|.//p/span/text()")        # 版本1.0，没有考虑到有的页面中会多出span标签
    # text_list = zoom.xpath(".//p/span/text()|.//p/text()")        # 版本2.0，没有考虑到有的页面中会缺少标签
    text_list = zoom.xpath(".//text()")                             # 版本3.0，直接获取页面中的文本，进行过滤

    for (index, text) in enumerate(text_list):
        # print(text)
        if text.startswith("◎译　　名"):
            movie["teanslation_title"] = text.replace("◎译　　名", "").strip()
        elif text.startswith("◎片　　名"):
            movie["real_title"] = text.replace("◎片　　名", "").strip()
        elif text.startswith("◎年　　代"):
            movie["time"] = text.replace("◎年　　代", "").strip()
        elif text.startswith("◎产　　地"):
            movie["place"] = text.replace("◎产　　地", "").strip()
        elif text.startswith("◎类　　别"):
            movie["category"] = text.replace("◎类　　别", "").strip()
        elif text.startswith("◎语　　言"):
            movie["language"] = text.replace("◎语　　言", "").strip()
        elif text.startswith("◎上映日期"):
            movie["release_time"] = text.replace("◎上映日期", "").strip()
        elif text.startswith("◎豆瓣评分"):
            movie["douban_score"] = text.replace("◎豆瓣评分", "").strip()
        elif text.startswith("◎片　　长"):
            movie["length"] = text.replace("◎片　　长", "").strip()
        elif text.startswith("◎导　　演"):
            movie["director"] = text.replace("◎导　　演", "").strip()
        elif text.startswith("◎主　　演"):
            actors = []
            actors.append(text.replace("◎主　　演", "").strip())
            for num in range(index + 1, index + 10):
                if (text_list[num].startswith("◎简　　介")):
                    break
                else:
                    actors.append(text_list[num].strip())
            movie["actors"] = actors
        elif text.startswith("◎简　　介"):
            conttent_index = index + 1
            movie["introduction"] = text_list[conttent_index].strip()

    if len(zoom.xpath(".//td/a/@href")) > 0:
        download_url = zoom.xpath(".//td/a/@href")[0]
    elif len( zoom.xpath(".//td//a/@href")) > 0 :
        download_url = zoom.xpath(".//td//a/@href")[-1]
    else:
        download_url = "爬取失败，手动修改！"

    movie["download_url"] = download_url
    #print("·", end=" ")
    return movie


def get_movie():
    page_urls = movie_list_page()
    movies=[]
    res=""
    for (index, page_url) in enumerate(page_urls):

        movie_detail_urls = get_detail_url(page_url)

        for movie_detail_url in movie_detail_urls:
            movie_content = get_movie_content(movie_detail_url)
            #print(movie_content)
            if movie_content and 'douban_score' in movie_content:
                scores = movie_content['douban_score'].split("/")
                score = float(scores[0])
                if score >= 7.2: #豆瓣评分7.2以上才可以推荐
                    movies.append(movie_content)
    if movies:
        random.shuffle(movies)
        movie = movies[0]
        title = ""
        if movie['place'] == '中国大陆':
            title = movie['real_title'].split('/')[0]
        else:
            title = movie['teanslation_title'].split('/')[0]
        res="为您推荐"+movie['time']+"年在"+movie['place']+"上映的电影"+title+"。它主要讲了"+movie['introduction']
    else:
        res="最近没啥好康的电影"
    return res




