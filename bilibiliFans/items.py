# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class bfansItem(Item):
    # define the fields for your item here like:
    # name = Field()
    mid = Field()
    name = Field()
    birthday = Field()
    fans = Field()
    place = Field()
    sex = Field()
    sign = Field()
    attention = Field()

