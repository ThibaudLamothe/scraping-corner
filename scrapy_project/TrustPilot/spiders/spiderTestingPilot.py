# Scraping imports
import scrapy
from TrustPilot.spiders import get_info

# Classic imports
import datetime

# Logging imports
from logzero import logger


class TrustPilotSpiderTest(scrapy.Spider):
    name = "TrustPilotTest"

    def start_requests(self):
        url = 'https://fr.trustpilot.com/categories/bank'
        yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):

        # Number of main page scrapped
        logger.warn('Parse page ({})')

        # Get the url of each reference on the current page
        links = get_info.get_article_urls(response)

        # Get pagination information
        next_page = get_info.get_next_page_of_articles(response)
        next_page_number = get_info.get_next_page_number(next_page)

           

    def parse_articles(self, response):
        
        # Number of reviews scrapped
        logger.info('Parse object ({})')
        logger.debug(response.url)

        # Get institute name
        institute = get_info.get_institute(response)

        # Go through all reviews of the list
        reviews = get_info.get_reviews(response)
        review = reviews[0]
        
        auteur  = get_info.get_review_auteur(review)
        rating = get_info.get_review_rating(review)
        title = get_info.get_review_title(review)
        auteur_nb_review = get_info.get_nb_reviews_auteur(review)
        date_review = get_info.get_review_date(review)
        nb_answers = get_info.is_answers_to_review(review)
        content = get_info.get_review_content(review)
        url = get_info.get_review_url(review)


        # Get pagination information
        next_page = get_info.get_next_page_of_reviews(response)
        next_page_number = get_info.get_next_page_number(next_page)