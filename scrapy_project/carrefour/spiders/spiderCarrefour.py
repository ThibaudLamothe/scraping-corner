# Scrapy imports
import scrapy
from Carrefour.spiders import get_info
from Carrefour.items import ArticleItem
from scrapy_splash import SplashRequest

# Logging imports
import logging
import logzero
from logzero import logger
logzero.loglevel(logging.INFO)


################################################################
################################################################
#                          ABOUT SPLASH                        #
################################################################
################################################################

# Carrefour's website use javascript,
# which is not well tackled by scrapy
# Then we use splash to load the full webpages

# Documentation
# https://splash.readthedocs.io/en/stable/install.html

# Run on docker
# docker pull scrapinghub/splash
# docker run -p 8050:8050 scrapinghub/splash

# Blog explanation
# http://scrapingauthority.com/scrapy-javascript
# pip install scrapy-splash

################################################################
################################################################
################################################################



class SpiderCarrefour(scrapy.Spider):
    name = "CarrefourSpider"

    def __init__(self, *args, **kwargs):
        super(SpiderCarrefour, self).__init__(*args, **kwargs)

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

        # Compteur for parsing indications
        self.page = 0
        self.object = 0


    def start_requests(self):

        # Defining the number of pages to scrap
        nb_articles = 7856
        nb_article_par_page = 60
        nb_page = int(nb_articles / nb_article_par_page)
        # nb_page = 2

        # Going to each pages
        for page in range(1, nb_page + 1):
            url = 'https://www.carrefour.fr/r?page={}'.format(page)
            logger.warn(url)

            yield SplashRequest(url=url, callback=self.parse, args={'wait':5})


    def parse(self, response):

        # Displaying parsing information
        self.page +=1
        logger.error('> Pages loaded {} : {}'.format(self.page, response.url))

        # Extracting product links on articles page
        urls = get_info.get_links(response)

        # Going to the articles pages
        for url in urls:
            url = 'https://www.carrefour.fr' + url
            yield SplashRequest(url=url, callback=self.parse_article, args={'wait':10})


    def parse_article(self, response):

        # Displaying parsing information
        self.object += 1
        logger.warn('> Articles scrapped {}'.format(self.object))

        # Creating item with scraped information
        item = ArticleItem()

        item['description'] = get_info.get_description(response)
        item['description2'] = get_info.get_description2(response)
        item['titre'] = get_info.get_titre(response)
        item['soustitre'] = get_info.get_soustitre(response)
        item['similaire'] = get_info.get_similaire(response)
        item['price'] = get_info.get_price(response)
        item['image_urls'] = get_info.get_picture_url(response)
        item['position'] = get_info.get_position(response)
        item['url'] = response.url

        # Depending on loglevel, display key/values
        for key, value in item.items():
            logger.debug(key)
            logger.debug(value)

        # Save item in specified file
        yield item




