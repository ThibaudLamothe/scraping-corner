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
    nb_views = scrapy.Field()
    description = scrapy.Field()
    ingredient_dict = scrapy.Field()
    equipment_dict = scrapy.Field()
    how_to_make_dict = scrapy.Field()
    similar_recipes_dict = scrapy.Field()
    

