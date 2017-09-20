from elasticsearch_dsl import DocType, Keyword, Text
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class ImageType(DocType):
    name = Text() # 图片的文件名
    title = Text(analyzer="ik_max_word") # 图片的标题
    source = Text() # 图片的来源
    url = Keyword() # 图片的url地址
    local_path = Text() # 本地保存的路径

    class Meta:
        doc_type = "image"
        index = "image"

if "__name__" == "__main__":
    ImageType.init()