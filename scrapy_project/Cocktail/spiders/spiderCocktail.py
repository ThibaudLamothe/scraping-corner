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
        logger.warn('> PARSING NEW MAIN PAGE OF COCKTAILS ({})'.format(self.main_nb))

        self.main_nb += 1

        # Get the list of these 30 restaurants
        my_urls = get_info.get_urls_cocktails_in_main_search_page(response)
        for urls in my_urls:
            yield response.follow(url=urls, callback=self.parse_cocktail)
            # logger.info(my_urls)
        

        next_page, next_page_number = get_info.get_urls_next_list_of_cocktails(response)

        if get_info.go_to_next_page(next_page, next_page_number, self.max_page):
            yield response.follow(next_page, callback=self.parse)

    def parse_cocktail(self, response):
        """REAL PARSING : Open a specific page with restaurant description
            - Read these data and store them
        """
        self.cocktail_nb += 1
        logger.info('> COCKTAIL  ({}) = {}'.format(self.cocktail_nb, response.url))

        # Intitiate storing object
        cocktail_item = CocktailItem()
        ingredients = get_info.get_ingredients_panel(response)

        # URL
        cocktail_item['name']           = get_info.get_cocktail_name(response)
        cocktail_item['url']            = get_info.get_url(response)
        cocktail_item['picture_url']    = get_info.get_cocktail_picture_url(response)
        cocktail_item['level']          = get_info.get_cocktail_level(response)
        cocktail_item['rating']         = get_info.get_cocktail_rating(response)
        cocktail_item['nb_reviews']     = get_info.get_cocktail_nb_reviews(response)
        cocktail_item['description']    = get_info.get_cocktail_description(response)
        cocktail_item['alcool_lvl']     = get_info.get_cocktail_alcool_quantity(ingredients)
        cocktail_item['ingredients']    = get_info.get_cocktail_ingredient_dict(ingredients)
        cocktail_item['equipments']     = get_info.get_cocktail_equipment_dict(response)
        cocktail_item['instructions']   = get_info.get_cocktail_instructions_list(response)
        cocktail_item['tags']           = get_info.get_cocktail_tags(response)
        yield cocktail_item

    
    
    
    
   
    
    
   
    
    
    
    
