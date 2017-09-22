# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import os
import pymongo

from image_spider.modules.es_types import ImageType
from w3lib.html import remove_tags
from scrapy.exporters import JsonItemExporter

class ImageSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    # 自定义的json导出方法
    def __init__(self):
        self.file = codecs.open('image_info.json', 'w', encoding='utf-8')
    def process_item(self, item, spdier):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()

class JsonExporterPipeline(object):
    # 导出json文件
    def __init__(self):
        self.file = open('image_export.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class GetImagesPipeline(object):
    def __init__(self):
        localPath = 'download_img'
        if not os.path.exists(localPath):
            os.mkdir(localPath)
        os.chdir(localPath)

class ElasticsearchPipeline(object):

    def process_item(self, item, spider):
        image = ImageType()
        image.title = remove_tags(item['title'])
        image.local_path = item['local_path']

        image.save()
        return item

class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item