# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
from scrapy import signals



class bfansMiddleware:
    logger = logging.getLogger(__name__)
    def __init__(self):
        self.change_ip = 0

    def process_request(self, request, spider):
        if self.change_ip:
            request.meta['proxy'] = 'http://123.206.17.241:8888'
        return None

    def process_response(self, request, response, spider):
        if response.status == 403:
            self.logger.debug('ip 被封 尝试换ip')
            request.meta['proxy'] = 'http://123.206.17.241:8888'
            return request
        return response
    # def process_exception(self, request, exception, spider):
    #    self.logger.debug('Get exception')
    #   return request

