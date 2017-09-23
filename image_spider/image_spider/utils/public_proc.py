import requests
import codecs
import json

def download_url(save_path, url):
    # 下载文件方法
    print('正在下载：%s' % url)
    ir = requests.get(url)
    open(save_path, 'wb').write(ir.content)

class JsonWithEncodingPipeline(object):
    # 将item作为json的格式导出
    def __init__(self, item):
        self.file = codecs.open('dump.jl', 'a', encoding="utf-8")
        self.process_item(item)

    def process_item(self, item):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        self.spider_closed()

    def spider_closed(self):
        self.file.close()


class ElasticsearchPipeline(object):
    # 将item数据保存到es中
    def __init__(self, item):
        self.process_item(item)

    def process_item(self, item):
        #将item转换为es的数据
        item.save_to_es()
        return item

def save_item_to_es(item):
    print("\nsave_to_es()\n")
    item.save_to_es()