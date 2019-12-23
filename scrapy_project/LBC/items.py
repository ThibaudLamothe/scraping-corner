# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LbcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AnnonceItem(scrapy.Item):
    # define the fields for your item here like:
    
    id_ = scrapy.Field()
    url = scrapy.Field()
    titre = scrapy.Field()
    description = scrapy.Field()
    prix = scrapy.Field()
    date_absolue = scrapy.Field()
    auteur = scrapy.Field()
    ville = scrapy.Field()
    code_postal = scrapy.Field()
    is_msg = scrapy.Field()
    is_num = scrapy.Field()
    critere = scrapy.Field()
    nb_pict  = scrapy.Field()
    categorie = scrapy.Field()
    