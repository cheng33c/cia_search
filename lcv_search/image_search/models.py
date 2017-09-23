from elasticsearch_dsl import DocType, Keyword, Text, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as ca

connections.create_connection(hosts=["localhost"])

class CustomAnalyzer(ca):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

class ImageType(DocType):
    url_object_id = Keyword() # 图片对象id
    local_path = Text() # 图片路径
    source = Text() # 图片的来源
    url = Keyword() # 图片的url地址
    tags = Text(analyzer='ik_max_word') # 图片生成的标签
    suggest = Completion(analyzer=ik_analyzer) # 搜索建议

    class Meta:
        index = "baidu"
        doc_type = "image"

if __name__ == "__main__":
    ImageType.init()