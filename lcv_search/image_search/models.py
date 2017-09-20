from django.db import models
from elasticsearch_dsl import DocType, Keyword, Text
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class ImageType(DocType):
    name = Text() # 图片的文件名
    title = Text(analyzer="ik_max_word") # 图片的标题
    tags = Text() # 图片的分类
    source = Text() # 图片的来源
    url = Keyword() # 图片的url地址
    local_path = Text() # 本地保存的路径