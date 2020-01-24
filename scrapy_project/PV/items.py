# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PVItem(scrapy.Item):
    # define the fields for your item here like:

    titre = scrapy.Field()
    id_ = scrapy.Field()
    prix = scrapy.Field()
    small_description = scrapy.Field()
    surface = scrapy.Field()
    ville = scrapy.Field()
    code_postal = scrapy.Field()
    nb_pieces = scrapy.Field()
    nb_pict = scrapy.Field()
    agence = scrapy.Field()
    url = scrapy.Field()