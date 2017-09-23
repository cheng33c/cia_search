# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    url_object_id = scrapy.Field()
    source = scrapy.Field() # 图片来源
    url = scrapy.Field() # 图片网址
    local_path = scrapy.Field() # 本地路径
    tags = scrapy.Field() # 图片标签