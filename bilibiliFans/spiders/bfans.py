# -*- coding: utf-8 -*-
import json
import re

import requests
import time
from scrapy import FormRequest, Request, Spider, Selector
from bilibiliFans.items import bfansItem
import logging



class BfansSpider(Spider):
    name = "bfans"
    follower_url = 'http://api.bilibili.com/x/relation/followers?vmid={mid}&pn={page}&ps=100'
    following_url = 'http://api.bilibili.com/x/relation/followings?vmid={mid}&pn={page}&ps=100'
    post_url = 'http://space.bilibili.com/ajax/member/GetInfo'
    start_user_mid = '2697177'
    proxy = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Referer': '',
    }
    data = {
        'mid': '',
        'csrf':'d120d2c81189882ea7d9c9155fdd9df6',
    }

    def start_requests(self):
        self.headers['Referer'] = 'https://space.bilibili.com/' + self.start_user_mid+'/'
        page1 = 1
        page2 = 1
        flag1 = 1
        flag2 = 1

        while page1 <= 5 and flag1:
            yield Request(url=self.follower_url.format(mid=self.start_user_mid, page=page1),callback=self.parse_mid, headers=self.headers)
            page1+=1
        while page2 <= 5 and flag2:
            yield Request(url=self.following_url.format(mid=self.start_user_mid, page=page2), callback=self.parse_mid, headers=self.headers)
            page2+=1


    def parse_mid(self, response):
        content = response.text
        mid_list = re.findall('"mid":(\d+?),',content)
        self.proxy = 'http://' + requests.get('http://123.206.17.241:8000/first').text
        for mid in mid_list:
            self.data['mid'] = mid
            self.headers['Referer'] = 'https://space.bilibili.com/' + str(mid) + '/'
            print('Using ip:'+ self.proxy)
            yield FormRequest(url=self.post_url, meta={'proxy':self.proxy},headers=self.headers, formdata=self.data, callback=self.parse_user)


    def parse_user(self, response):
        try:
            self.proxy = 'http://' + requests.get('http://123.206.17.241:8000/first').text
            content = json.loads(response.text)
            item = bfansItem()
            data = content['data']
            item['name'] = data.get('name')
            item['mid'] = data.get('mid')
            item['sex'] = data.get('sex')
            item['place'] = data.get('place')
            item['fans'] = data.get('fans')
            item['birthday'] = data.get('birthday')
            item['sign'] = data.get('sign')
            yield item
        except Exception as e:
            print(e.args)




