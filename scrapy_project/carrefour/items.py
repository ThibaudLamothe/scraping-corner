# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    description = scrapy.Field()
    description2 = scrapy.Field()
    titre = scrapy.Field()
    soustitre = scrapy.Field()
    similaire = scrapy.Field()
    price = scrapy.Field()
    position = scrapy.Field()
    image_urls = scrapy.Field()
    image_name = scrapy.Field()
    # images = scrapy.Field()