# Scraping imports
import time
import scrapy
from logzero import logger
from Amazon.spiders import get_info


#############################################################################
#############################################################################
#############################################################################


class SpiderAmazonTestingMain(scrapy.Spider):
    name = "SpiderAmazonTestingMain"

    def start_requests(self):
        url = 'http://amazon.com/s?i=sporting-intl-ship&rh=n%3A%2116225014011&page=2&qid=1581438225&ref=lp_16225014011_pg_2'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        logger.error('--- STARTING MAIN UNIT TESTING ---')
        
        # Get the url of each reference on the current page
        links = get_info.get_reference_links(response)
        logger.info(len(links))
        logger.info(links[0])
        assert len(links) == 24,                                            'get_info.get_reference_links -- links'


        # Get pagination information
        next_page, page_number = get_info.get_main_pagination(response)
        logger.info('Next page : {}'.format(next_page))
        logger.info('Page number : {}'.format(page_number))
        assert type(next_page) == str,                                      'get_info.get_main_pagination -- next page'
        assert '/s?i=sporting-intl-ship&rh=n%3A16225014011&' in next_page,  'get_info.get_main_pagination -- next page'
        assert page_number == 2,                                            'get_info.get_main_pagination --  page number'
        
        logger.error('--- MAIN UNIT TESTING IS OK ---')
        time.sleep(3)
      

#############################################################################
#############################################################################
#############################################################################


class SpiderAmazonTestingReference(scrapy.Spider):
    name = "AmazonSpiderTestingReference"

    def start_requests(self):
        url = 'http://amazon.com/Fruit-Loom-womens-Pullover-heather/dp/B07KL1L7YH/ref=sr_1_25?dchild=1&qid=1584802115&s=sporting-goods&sr=1-25'
        yield scrapy.Request(url=url, callback=self.parse_reference)

    def parse_reference(self, response):
        
        logger.error('--- STARTING REFERENCE UNIT TESTING ---')

        # Get price informations
        prices_list = get_info.get_prices(response)
        full_none = [i for i in prices_list if i is not None]
        logger.info('Prices')
        logger.info(prices_list)
        logger.info(full_none)
        assert len(full_none) > 0,                                          'get_info.get_main_pagination -- next page'
        
        # Get title information
        title = get_info.get_title(response)
        logger.debug(title)
        supposed_title = "Fruit of the Loom Women's Cotton Pullover Sport Bra(Pack of 3)"
        assert title == supposed_title,                                     'get_info.get_title'
        assert type(title)==str,                                            'get_info.get_title'

        # Get description information
        description = get_info.get_description(response)
        logger.debug('Description')
        assert type(description)==str,                                      'get_info.get_description'
        
        # Get item description information
        items_description = get_info.get_items_description(response)    
        logger.debug('Description')
        assert type(items_description)==str,                                'get_info.get_items_description'
        
        # Get category information
        category = get_info.get_category(response)
        logger.debug('Category : {}'.format(category))
        assert type(category)==str,                                         'get_info.get_category'

        logger.error('--- REFERENCE UNIT TESTING IS OK ---')
        time.sleep(10)