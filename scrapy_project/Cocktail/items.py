# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CocktailItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    picture_url = scrapy.Field()
    level = scrapy.Field()
    rating = scrapy.Field()
    nb_reviews = scrapy.Field()
    description = scrapy.Field()
    alcool_lvl = scrapy.Field()
    ingredients = scrapy.Field()
    equipments = scrapy.Field()
    instructions = scrapy.Field()
    tags = scrapy.Field()
    

