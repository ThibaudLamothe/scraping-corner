# Scraping imports
import scrapy
from Amazon.spiders import get_info
from Amazon.items import AmazonItem
# from scrapy_splash import SplashRequest


# Logging import
import logzero
import logging
from logzero import logger

class SpiderAmazon(scrapy.Spider):
    name = "AmazonSpider"

    def __init__(self, *args, **kwargs):
        super(SpiderAmazon, self).__init__(*args, **kwargs)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:

            # Categories url for Hackathon
            self.start_urls = [
                'http://amazon.com/s?i=sporting-intl-ship&rh=n%3A%2116225014011&page=2&qid=1581438225&ref=lp_16225014011_pg_2' # sports & outdoors
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



    def parse_reference(self, response):
        self.object += 1
        get_info.print_separation(self.object)

        # Get price informations
        price_1, price_2, price_3, price_4, price_5 = get_info.get_prices(response)

        # Get title information
        title = get_info.get_title(response)

        # Get description information
        description = get_info.get_description(response)

        # Get item description information
        items_description = get_info.get_items_description(response)

        # Get category information
        category = get_info.get_category(response)

        # Create item
        item = AmazonItem()
        item['price_1'] = price_1
        item['price_2'] = price_2
        item['price_3'] = price_3
        item['price_4'] = price_4
        item['price_5'] = price_5
        item['category'] = category
        item['choice_scrap'] = 'sports'
        item['titre'] = title
        item['items'] = items_description
        item['description'] = description
        item['url'] = response.url

        # Display results
        for key, value in item.items():
            print('> ', key.upper(), '\n')
            print(value)

        # Store value as decided in the pipeline
        yield item
