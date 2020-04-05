# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# ************************        ADAPAT YOUR ITEM            ****************************

class OmsItem(scrapy.Item):
    
    scraping_time = scrapy.Field()
    url = scrapy.Field()
    field_1 = scrapy.Field()
    field_2 = scrapy.Field()
    field_3 = scrapy.Field()