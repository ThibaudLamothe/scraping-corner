# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelreviewsItem(scrapy.Item):
    # define the fields for your item here like:
    rating = scrapy.Field()
    review = scrapy.Field()
    title = scrapy.Field()
    trip_date = scrapy.Field()
    trip_type = scrapy.Field()
    published_date = scrapy.Field()
    image_url = scrapy.Field()
    hotel_type = scrapy.Field()
    hotel_name = scrapy.Field()
    hotel_adress = scrapy.Field()
    price_range = scrapy.Field()
    reviewer_id = scrapy.Field()
    review_id = scrapy.Field()
    review_language = scrapy.Field()
    pid = scrapy.Field()
    locid = scrapy.Field()
    sentiment = scrapy.Field()
