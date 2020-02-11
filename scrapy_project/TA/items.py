# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewRestoItem(scrapy.Item):
    id_resto = scrapy.Field()
    id_comment = scrapy.Field()
    resto = scrapy.Field()
    resto_url = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    diner_date = scrapy.Field()
    rating_date = scrapy.Field()
    answer_text = scrapy.Field()
    reviewer_pseudo = scrapy.Field()
    reviewer_origin = scrapy.Field()
    reviewer_info_sup = scrapy.Field()
    other_ratings_category = scrapy.Field()
    other_ratings_value = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()


class RestoItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()
    name_url = scrapy.Field()
    titre = scrapy.Field()
    rating = scrapy.Field()
    nb_review = scrapy.Field()
    street_adress = scrapy.Field()
    locality = scrapy.Field()
    country = scrapy.Field()
    tel_number = scrapy.Field()
    # tel_number2 = scrapy.Field()
    url_menu = scrapy.Field()
    info_1 = scrapy.Field()
    info_2 = scrapy.Field()
    price_range = scrapy.Field()
    picture_number = scrapy.Field()
    avg_rating = scrapy.Field()
    nb_reviews = scrapy.Field()
    local_ranking = scrapy.Field()
    other_information = scrapy.Field()
    all_rankings = scrapy.Field()
    categories_ranking = scrapy.Field()
    description = scrapy.Field()
    details = scrapy.Field()
    rating_excellent = scrapy.Field()
    rating_very_good = scrapy.Field()
    rating_average = scrapy.Field()
    rating_poor = scrapy.Field()
    rating_terrible = scrapy.Field()



class HotelReviewsItem(scrapy.Item):
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


class TripAdvisorAirlineItem(scrapy.Item):
    title = scrapy.Field()
    rating=scrapy.Field()
    date=scrapy.Field()
    content=scrapy.Field()
    route=scrapy.Field()
    cabin=scrapy.Field()
    destination=scrapy.Field()
