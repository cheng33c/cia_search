# -*- coding: utf-8 -*-
import scrapy
import pymongo
import os
import requests
import re
import urllib.request

from .config import *

# MONGO CONFIG
MONGO_DB = 'image_spider'
MONGO_TABLE = 'baidu_pic'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

class BaiduPicSpider(scrapy.Spider):
    name = 'baidu_pic'
    allowed_domains = ['image.baidu.com']
    start_urls = ['https://image.baidu.com/search/acjson?']

    headers = {
        "HOST": "image.baidu.com",
        "Referer": "https://image.baidu.com",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0"
    }
    params = []
    # keyword = input("请输入你要爬取的图片")

    urls = []

    def __init__(self):
        pages = 10
        keyword = '人物 开心'
        for i in range(30, 30 * pages + 30, 30):
            self.params.append({
                'tn': 'resultjson_com',
                'ipn': 'rj',
                'ct': 201326592,
                'is': '',
                'fp': 'result',
                'queryWord': keyword,
                'cl': 2,
                'lm': -1,
                'ie': 'utf-8',
                'oe': 'utf-8',
                'adpicid': '',
                'st': -1,
                'z': '',
                'ic': 0,
                'word': keyword,
                's': '',
                'se': '',
                'tab': '',
                'width': '',
                'height': '',
                'face': 0,
                'istype': 2,
                'qc': '',
                'nc': 1,
                'fr': '',
                'pn': i,
                'rn': 30,
                'gsm': '1e',
                '1505488170554': ''
            })

    def start_requests(self):
        for i in self.params:
            self.urls.append(requests.get(self.start_urls[0], params=i).json().get('data'))
            new_url = self.start_urls[0]
            for (a, b) in i.items():
                new_url = new_url + "&" + str(a) + "=" + str(b)
            yield scrapy.Request(url=new_url, callback=self.parse)

        # self.getPic(self.urls, baidu_pic_path)

    def parse(self, response):
        for list in self.urls:
            for i in list:
                #print(i.get('fromPageTitleEnc').encode())
                #fromPageTitleEnc = i.get('fromPageTitleEnc').decode('utf-8')
                item = {
                    'thumbURL': i.get('thumbURL'),
                    'fromURLHost': i.get('fromURLHost'),
                }



    def getPic(self, dataList, localPath):
        if not os.path.exists(localPath):
            os.mkdir(localPath)
        os.chdir(localPath)
        try:
            x = 0
            for list in dataList:
                for i in list:
                    if i.get('thumbURL') != None:
                        print('正在下载：%s' % i.get('thumbURL'))
                        ir = requests.get(i.get('thumbURL'))
                        open(localPath + '%d.jpg' % x, 'wb').write(ir.content)
                        x += 1
            print('图片下载完成')
        except Exception:
            print("图片下载失败")