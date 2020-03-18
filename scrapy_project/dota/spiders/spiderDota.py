# Scraping imports
import scrapy
from Amazon.spiders import get_info
from Amazon.items import AmazonItem
# from scrapy_splash import SplashRequest


# Logging import
import logzero
import logging
from logzero import logger

class SpiderDota(scrapy.Spider):
    name = "dota"

    def __init__(self, *args, **kwargs):
        super(SpiderAmazon, self).__init__(*args, **kwargs)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:

            # Categories url for Hackathon
            self.start_urls = [
               'https://liquipedia.net/dota2/Portal:Patches#Dota_2'
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

        # Scrapping compteur
        self.page = 0
        self.object = 0


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # yield SplashRequest(url=url, callback=self.parse, args={'wait':2})


    def parse(self, response):

        # Number of main page scrapped
        self.page += 1

        # Get the url of each reference on the current page
        links = get_info.get_reference_links(response)

        # Follow these urls
        for link in links:
            yield response.follow(url=link, callback=self.parse_reference)
            # link = 'https://www.amazon.com' + link
            # yield SplashRequest(url=link, callback=self.parse_reference, args={'wait':5})


        # Get pagination information
        next_page, page_number = get_info.get_main_pagination(response)

        # Decision to follow a page or not
        if page_number <= 120:
            yield response.follow(next_page, callback=self.parse)
            # next_page = 'https://www.amazon.com' + next_page
            # yield SplashRequest(url=next_page, callback=self.parse, args={'wait':10})
