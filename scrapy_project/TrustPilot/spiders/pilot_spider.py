# Scraping imports
import scrapy
from TrustPilot.items import TrustpilotItem
from TrustPilot.spiders import get_info

# Classic imports
import datetime

# Logging imports
import logzero
import logging
from logzero import logger
logzero.loglevel(logging.DEBUG) # To display content information
logzero.loglevel(logging.INFO)  # To see number of parsed references
#logzero.loglevel(logging.WARN)  # To see number of parsed main pages


class TrustPilotSpider(scrapy.Spider):
    name = "TrustPilot"

    def __init__(self, *args, **kwargs):
        super(TrustPilotSpider, self).__init__(*args, **kwargs)

        # Main url to scrap
        self.start_urls = [
            # 'https://fr.trustpilot.com/categories/bank',
            'https://fr.trustpilot.com/categories/money_insurance?numberofreviews=0&timeperiod=0',
            
        ]
        
        # Scrapping compteur
        self.page = 0
        self.object = 0
        self.max_page_articles = 100000
        self.max_page_reviews = 100000
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
            yield response.follow(url=link, callback=self.parse_articles)
          
        # Get pagination information
        next_page = get_info.get_next_page_of_articles(response)
        next_page_number = get_info.get_next_page_number(next_page)
        logger.error(next_page)
        logger.error(next_page_number)

        # Decision to follow a page or not
        if get_info.go_to_next_page(next_page, next_page_number, self.max_page_articles):
            yield response.follow(next_page, callback=self.parse)
           

    def parse_articles(self, response):
        
        # Number of reviews scrapped
        self.object += 1
        logger.info('Parse object ({})'.format(self.object))
        logger.debug(response.url)

        # Get institute name
        institute = get_info.get_institute(response)


        # Go through all reviews of the list
        reviews = get_info.get_reviews(response)
        
        for review in reviews:
            
            # Instantiate item
            item = TrustpilotItem()

            item['institute'] = institute
            item['auteur']  = get_info.get_review_auteur(review)
            item['rating'] = get_info.get_review_rating(review)
            item['title'] = get_info.get_review_title(review)
            item['auteur_nb_review'] = get_info.get_nb_reviews_auteur(review)
            item['date_review'] = get_info.get_review_date(review)
            item['date_scrapping'] = self.scrapping_time
            item['nb_answers'] = get_info.is_answers_to_review(review)
            item['content'] = get_info.get_review_content(review)
            item['url'] = get_info.get_review_url(review)
            
            logger.debug(item['title'])
            # Store value as decided in the pipeline
            yield item

        # Get pagination information
        next_page = get_info.get_next_page_of_reviews(response)
        next_page_number = get_info.get_next_page_number(next_page)

        # Decision to follow a page or not
        if get_info.go_to_next_page(next_page, next_page_number, self.max_page_reviews):
            yield response.follow(next_page, callback=self.parse_articles)
