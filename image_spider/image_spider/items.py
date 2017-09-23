# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from image_spider.modules.es_types import *


class ImageSpiderItem(scrapy.Item):

    # define the fields for your item here like:
    url_object_id = scrapy.Field()
    source = scrapy.Field() # 图片来源
    url = scrapy.Field() # 图片网址
    local_path = scrapy.Field() # 本地路径
    tags = scrapy.Field() # 图片标签

    def save_to_es(self):
        image = ImageType()
        image.meta.id = self["url_object_id"]
        image.local_path = self["local_path"]
        image.tags = self["tags"]
        image.url = self["url"]
        image.source = self["source"]

        image.save()
        return