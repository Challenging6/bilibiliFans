# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging

import time
from scrapy import signals
import requests
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import random
import scrapy.exceptions
class bfansMiddleware:
    logger = logging.getLogger(__name__)
    ip = None
    list = ['123.206.17.241:8888', '']

    def process_request(self, request, spider):
        if request.meta.get('proxy'):
            try:
                print('Using ip:'+ str(request.meta.get('proxy')))
            except Exception as e:
                print(e.args)

        else:
            try:
                ip = 'http://' + requests.get('http://123.206.17.241:8000/first').text
                request.meta['proxy'] = ip
            except Exception as e:
                print(e.args)
                print('Using' + ' localhost')
        return None
    def process_response(self, request, response, spider):
        if response.status != 200:
            print(str(response.status)+' Retrying')
            new_request = request.copy()
            ip = 'http://' + requests.get('http://123.206.17.241:8000/first').text
            while ip == request.meta['proxy']:
                print('Waiting for changing ip')
                time.sleep(1)
                ip = 'http://' + requests.get('http://123.206.17.241:8000/first').text
            new_request.dont_filter = True
            new_request.meta['proxy'] = ip
            return new_request
        return response

    def process_exception(self, request, exception, spider):
        ip = ''
        while ip == request.meta['proxy']:
            time.sleep(1)
            ip = 'http://' + requests.get('http://123.206.17.241:8000/first').text
        new_request = request.copy()
        new_request.meta['proxy'] = ip
        new_request.dont_filter = True
        return new_request