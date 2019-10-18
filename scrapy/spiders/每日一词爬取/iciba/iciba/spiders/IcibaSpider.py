# -*- coding: utf-8 -*-
import scrapy
import json

from iciba.items import IcibaItem


class IcibaspiderSpider(scrapy.Spider):
    name = 'IcibaSpider'
    # allowed_domains = ['news.iciba.com/views/dailysentence/daily.html#!/detail/title/2019-06-04']
    # start_urls = ['http://news.iciba.com/views/dailysentence/daily.html#!/detail/title/2019-06-04/']

    def start_requests(self):
        start_url = 'http://sentence.iciba.com/?&c=dailysentence&m=getdetail&title=2019-06-06'
        yield scrapy.Request(start_url, callback=self.parse)

    def parse(self, response):
        items = IcibaItem()
        json_obj = json.loads(response.body.decode('utf8'),encoding='utf-8')
        items['content'] = json_obj.get('content')
        items['last_title'] = json_obj.get('last_title')
        items['title'] = json_obj.get('title')
        items['note'] = json_obj.get('note')
        items['picture'] = json_obj.get('picture2')
        items['translation'] = json_obj.get('translation')
        last_title = items['last_title']
        title = items['title']
        next_url = "http://sentence.iciba.com/?&c=dailysentence&m=getdetail&title=" + last_title
        if title =="2017-12-31":
            pass
        else:
            yield items
            yield scrapy.Request(url=next_url, callback=self.parse)
