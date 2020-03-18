# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):

    # define the fields for your item here like:
    price_1 = scrapy.Field()
    price_2 = scrapy.Field()
    price_3 = scrapy.Field()
    price_4 = scrapy.Field()
    price_5 = scrapy.Field()
    category = scrapy.Field()
    choice_scrap = scrapy.Field()
    titre = scrapy.Field()
    items = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    