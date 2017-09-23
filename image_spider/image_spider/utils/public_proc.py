import requests
import codecs
import json

def download_url(save_path, url):
    # 下载文件方法
    print('正在下载：%s' % url)
    ir = requests.get(url)
    open(save_path, 'wb').write(ir.content)

class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self, item):
        self.file = codecs.open('dump.jl', 'a', encoding="utf-8")
        self.process_item(item)

    def process_item(self, item):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        self.spider_closed()

    def spider_closed(self):
        self.file.close()