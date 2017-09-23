# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from image_spider.modules.es_types import *
from elasticsearch_dsl.connections import connections

es = connections.create_connection(ImageType._doc_type.using)

def generator_suggests(index, info_tuple):
    # 根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter':["lowercase"]}, body=text)
            analyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = analyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words), "weight":weight})

    return suggests

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
        image.suggest = generator_suggests(ImageType._doc_type.index, ((image.tags, 10), (image.source, 3)))
        image.save()
        return