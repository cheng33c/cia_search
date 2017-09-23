from elasticsearch_dsl import DocType, Keyword, Text
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])

class ImageType(DocType):
    # url_object_id = Keyword() # 图片对象id
    local_path = Text() # 图片路径
    source = Text() # 图片的来源
    url = Keyword() # 图片的url地址
    tags = Text(analyzer='ik_max_word')

    class Meta:
        index = "baidu"
        doc_type = "image"

if __name__ == "__main__":
    ImageType.init()