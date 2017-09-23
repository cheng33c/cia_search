import requests
import codecs
import json
import hashlib

def download_url(save_path, url):
    # 下载文件方法
    print('正在下载：%s' % url)
    ir = requests.get(url)
    open(save_path, 'wb').write(ir.content)

def dump_item_to_json(item):
    # 将item导出为json文件
    file = codecs.open('dump.json', 'a', encoding='utf8')
    lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
    file.write(lines)
    file.close()

def get_md5(url):
    # 将url哈希
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def save_item_to_es(item):
    # 保存item到es中
    item.save_to_es()