# -*- coding: utf-8 -*-
import scrapy
import os
import urllib.request
import urllib.parse

from lxml import etree
from .config import *
from image_spider.utils.public_proc import *
from image_spider.items import ImageSpiderItem

class BaiduPicSpider(scrapy.Spider):
    name = 'baidu_pic'
    allowed_domains = ['image.baidu.com']
    start_urls = ['https://image.baidu.com/search/acjson?',
                  'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fr=&sf=1&fmq=1462357247335_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=']

    headers = {
        "HOST": "image.baidu.com",
        "Referer": "https://image.baidu.com",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0"
    }
    params = []
    # keyword = input("请输入你要爬取的图片")
    keyword = '悲伤'


    urls = []

    def __init__(self):
        # 第一次请求网页并解析爬取
        # 因为第一次没有ajax请求，所以直接进行访问爬取
        #self.keyword = urllib.parse.quote(self.keyword)
        #url = self.start_urls[1] + self.keyword
        #res = urllib.request.urlopen(url)
        #html = res.read()
        #page = etree.HTML(html.lower().decode('utf-8'))
        #images = page.xpath(u'//*[@id="imgid"]/*[@class="imglist"]/li')
        #for image in images:
        #    print(image)

        # 生成必要的参数并构造ajax请求
        pages = 10
        for i in range(30, 30 * pages + 30, 30):
            self.params.append({
                'tn': 'resultjson_com',
                'ipn': 'rj',
                'ct': 201326592,
                'is': '',
                'fp': 'result',
                'queryWord': self.keyword,
                'cl': 2,
                'lm': -1,
                'ie': 'utf-8',
                'oe': 'utf-8',
                'adpicid': '',
                'st': -1,
                'z': '',
                'ic': 0,
                'word': self.keyword,
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
        if not os.path.exists(baidu_pic_path):
            os.mkdir(baidu_pic_path)
        os.chdir(baidu_pic_path)

    def start_requests(self):
        for i in self.params:
            self.urls.append(requests.get(self.start_urls[0], params=i).json().get('data'))
            new_url = self.start_urls[0]
            for (a, b) in i.items():
                new_url = new_url + "&" + str(a) + "=" + str(b)
            yield scrapy.Request(url=new_url, callback=self.parse)



    def parse(self, response):
        item = ImageSpiderItem()
        try:
            x = 0
            for list in self.urls:
                for i in list:
                    thumbURL = i.get('thumbURL')
                    #print(i.get('fromPageTitleEnc').decode('utf-8'))
                    #fromPageTitleEnc = i.get('fromPageTitleEnc').decode('utf-8')
                    # 下载图片并保存
                    save_path = baidu_pic_path + '%d.jpg' % x
                    if thumbURL != None:
                        #download_url(save_path, thumbURL)
                        x += 1
                        # 建立item_loader
                        item['url'] = thumbURL
                        item['source'] = i.get('fromURLHost')
                        item['local_path'] = save_path
                        item['tags'] = self.keyword
                        item['url_object_id'] = get_md5(thumbURL)
                        dump_item_to_json(item)
                        save_item_to_es(item)
            print('图片下载完成')
        except Exception:
            print('图片下载失败')