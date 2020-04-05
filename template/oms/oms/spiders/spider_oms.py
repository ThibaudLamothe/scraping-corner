# Scraping imports
import scrapy
from oms.items import OmsItem
from oms.spiders import get_info

# Classic imports
import datetime

# Logging imports
from logzero import logger


class OMSSpider(scrapy.Spider):
    name = "OMS"

    def __init__(self, *args, **kwargs):
        super(OMSSpider, self).__init__(*args, **kwargs)

        # Main url to scrap
        self.start_urls = [
            ################################################################
            # YOUR URL(s) HERE
            # ... 
            ################################################################
        ]
        
        # Scrapping compteur
        self.page = 0
        self.object = 0
        self.max_page = 1000
        self.scrapping_time = str(datetime.datetime.now())[:19]
        

    def start_requests(self):
        for url in self.start_urls:
            logger.error(url)
            yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):

        # Number of main page scrapped
        self.page += 1
        logger.warn('Parse page ({})'.format(self.page))

        # Get the url of each reference on the current page
        links = get_info.get_article_urls(response)

        # Follow these urls
        for link in links:
            yield response.follow(url=link, callback=self.parse_article)
          
        # Get pagination information
        next_page = get_info.get_next_page_of_articles(response)        # LINK
        next_page_number = get_info.get_next_page_number(next_page)     # PAGE
        
        # Decision to follow a page or not
        if get_info.go_to_next_page(next_page, next_page_number, self.max_page_articles):
            yield response.follow(next_page, callback=self.parse)
           

    def parse_article(self, response):
        
        # Number of reviews scrapped
        self.object += 1
        logger.info('Parse object ({})'.format(self.object))
                    
        # Instantiate item
        item = OmsItem()

        # Always useful
        item['scraping_time'] = self.scrapping_time
        item['url'] =  response.url

        # Scraping items
        ################################################################################################
        item['field_1'] = get_info.get_field_1(response)
        item['field_2'] = get_info.get_field_2(response)
        item['field_3'] = get_info.get_field_3(response)
        ################################################################################################
    
        # Store value as decided in the pipeline
        yield item

    