# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrustpilotItem(scrapy.Item):
    # define the fields for your item here like:
    institute = scrapy.Field()
    auteur  = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    auteur_nb_review = scrapy.Field()
    date_review = scrapy.Field()
    date_scrapping = scrapy.Field()
    nb_answers = scrapy.Field()
    content =scrapy.Field()
    url = scrapy.Field()
    