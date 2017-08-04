# -*- coding: utf-8 -*-
import json

from scrapy import FormRequest, Request, Spider, Selector
from bilibiliFans.items import bfansItem


class BfansSpider(Spider):
    name = "bfans"
    post_url = 'https://space.bilibili.com/ajax/member/GetInfo'
    start_user_mid = '1398957'
    data = {
        'mid':start_user_mid,
        'csrf':'c326534f56f2f1714deefdbef7e477bc',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Referer': '',
    }

    def start_requests(self):
        self.headers['Referer'] = 'https://space.bilibili.com/'+self.start_user_mid+'/'
        yield FormRequest(url=self.post_url, headers=self.headers,formdata=self.data, callback=self.parse_user)
    #def make_requests_from_url(self, url):
    def parse_user(self, response):

        content = json.loads(response.text)
        item = bfansItem()
        print(content)
        #print(response.status)
        data = content['data']
        item['name'] = data.get('name')
        item['mid'] = data.get('mid')
        item['sex'] = data.get('sex')
        item['place'] = data.get('place')
        item['fans'] = data.get('fans')
        item['birthday'] = data.get('birthday')
        item['attention'] = data.get('attention')
        item['sign'] = data.get('sign')
        attentions = data.get('attentions')
        #print(attentions)
        yield item

        for mid in attentions:
            self.data['mid'] = str(mid)
            self.headers['Referer'] = 'https://space.bilibili.com/' + str(mid) + '/'
            yield FormRequest(url=self.post_url, headers=self.headers, formdata=self.data, callback=self.parse_user)

