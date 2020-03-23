# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LBCShortItem(scrapy.Item):
    titre = scrapy.Field()
    url = scrapy.Field()
    prix= scrapy.Field()
    categorie= scrapy.Field()
    lieu= scrapy.Field()
    date= scrapy.Field()
    nb_pict= scrapy.Field()


class LBCAnnonceItem(scrapy.Item):
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
    