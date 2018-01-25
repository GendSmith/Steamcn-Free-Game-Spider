import requests
from pymongo import MongoClient
from pyquery import PyQuery as pq
import re

#MongoDB服务器的创建
client = MongoClient()
db = client.steamcn1
sdb = db.steamcn1

def get_free_game_info(page):
    url = 'https://steamcn.com/forum.php?mod=forumdisplay&fid=319&orderby=dateline&typeid=469&orderby=dateline&typeid=469&filter=author&page='
    for i in range(page):
        newurl = url + str(i)
        print(newurl)
        html = requests.get(newurl).content.decode('utf-8')
        doc = pq(html)
        items = doc('#threadlisttableid tbody').items()
        prefix = 'https://steamcn.com/'
        for item in items:
            if item.find('.xst').attr('href'):
                homepageurl = prefix + str(item.find('.xst').attr('href'))
                if item.find('td.by.by-author > em >span').attr('title'):
                    publishDate = item.find('td.by.by-author > em >span').attr('title')+' 发表'
                else:
                    publishDate = item.find('td.by.by-author > em').text()
                product = {
                    'title':item.find('.xst').text(),
                    'homepage':homepageurl,
                    'publish_date': publishDate,
                }
                sdb.insert(product)
                print(product)

if __name__ =='__main__':
    get_free_game_info(184)
