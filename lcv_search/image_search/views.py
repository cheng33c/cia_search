import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from elasticsearch import Elasticsearch
from image_search.models import ImageType
from datetime import datetime

client = Elasticsearch(hosts=['127.0.0.1'])

# Create your views here.
class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s','')
        re_datas = []
        if key_words:
            s = ImageType.search()
            s = s.suggest('my_suggest', key_words, completion={
                "field":"suggest",
                "fuzzy":{"fuzziness":2},
                "size": 10
            })
            suggestions = s.execute_suggest()
            for match in suggestions.my_suggest[0].options:
                source = match._source
                re_datas.append(source["tags"])
        return HttpResponse(json.dumps(re_datas), content_type="application/json")

class SearchView(View):
    def get(self, request):
        key_words = request.GET.get("q", "")
        page = request.GET.get("p", "1")
        try:
            page = int(page)
            if page is 0:
                page = 1
        except:
            page = 1

        start_time = datetime.now() # 计时功能 输出查询时间
        response = client.search(
                    index="baidu",
                    body={
                        "query": {
                            "multi_match": {
                                "query": key_words,
                                "fields": ["source","url","tags"]
                            }
                        },
                        "from": (page-1)*10,
                        "size": 10,
                        "highlight": {
                            "pre_tags": ['<span class="keyWord">'],
                            "post_tags": ['</span>'],
                            "fields": {}
                        }
                    }
                )
        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()
        total_nums = response["hits"]["total"]
        if page % 10 > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)

        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            #if "tags" in hit["highlight"]:
              #  hit_dict["tags"] = "".join(hit["highlight"]["tags"])
            #else:
            hit_dict["tags"] = hit["_source"]["tags"]
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["source"] = hit["_source"]["source"]
            hit_dict["score"] = hit["_score"]

            hit_list.append(hit_dict)
        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds})