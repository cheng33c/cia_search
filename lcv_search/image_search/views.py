import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from image_search.models import ImageType
from elasticsearch import Elasticsearch
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
