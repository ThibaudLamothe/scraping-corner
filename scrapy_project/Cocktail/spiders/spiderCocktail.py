import scrapy
from Cocktail.spiders import get_info
from Cocktail.items import CocktailItem

import logging
import logzero
from logzero import logger


class Cocktail(scrapy.Spider):
    name = "spiderCocktail"

    def __init__(self, *args, **kwargs):
        super(Cocktail, self).__init__(*args, **kwargs)

        # Set logging level
        logzero.loglevel(logging.DEBUG)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:
            self.start_urls = [
                'https://uk.thebar.com/cocktail-recipes'
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

        # To track the evolution of scrapping
        self.main_nb = 0
        self.cocktail_nb = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """MAIN PARSING : Start from a classical restaurant page
            - Usually there are 30 restaurants per page
        """
        logger.warn('> PARSING NEW MAIN PAGE OF RESTO ({})'.format(self.main_nb))

        self.main_nb += 1

        # Get the list of these 30 restaurants
        my_urls = get_info.get_urls_cocktails_in_main_search_page(response)
        for urls in my_urls:
            # yield response.follow(url=urls, callback=self.parse_cocktail)
            logger.info(my_urls)
        

        next_page, next_page_number = get_info.get_urls_next_list_of_cocktails(response)

        if get_info.go_to_next_page(next_page, next_page_number, self.max_page):
            yield response.follow(next_page, callback=self.parse)

    def parse_cocktail(self, response):
        """REAL PARSING : Open a specific page with restaurant description
            - Read these data and store them
        """
        self.cocktail_nb += 1

        # Intitiate storing object
        cocktail_item = cocktail_item()

        # URL
        cocktail_item['name']                 = get_info.get__()
        cocktail_item['url']                  = get_info.get__()
        cocktail_item['picture_url']          = get_info.get__()
        cocktail_item['level']                = get_info.get__()
        cocktail_item['rating']               = get_info.get__()
        cocktail_item['nb_views']             = get_info.get__()
        cocktail_item['description']          = get_info.get__()
        cocktail_item['ingredient_dict']      = get_info.get__()
        cocktail_item['equipment_dict']       = get_info.get__()
        cocktail_item['how_to_make_dict']     = get_info.get__()
        cocktail_item['similar_recipes_dict'] = get_info.get__()
        yield cocktail_item
