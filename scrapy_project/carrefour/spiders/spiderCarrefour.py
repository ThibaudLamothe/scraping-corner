import scrapy
from carrefour.spiders import get_info
from carrefour.items import ArticleItem
from scrapy_splash import SplashRequest

from logzero import logger

class SpiderCarrefour(scrapy.Spider):
    name = "CarrefourSpider"


    def __init__(self, *args, **kwargs):
        super(SpiderCarrefour, self).__init__(*args, **kwargs)

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

        self.page = 0
        self.object = 0


    def start_requests(self):

        # Defining the number of pages to scrap
        nb_articles = 7856
        nb_article_par_page = 60
        nb_page = int(nb_articles / nb_article_par_page)
        nb_page = 2

        # Going to each pages
        for page in range(1, nb_page + 1):
            url = '> Start request : https://www.carrefour.fr/r?page={}'.format(page)
            logger.warn(url)
            yield SplashRequest(url=url, callback=self.parse) #, args={'wait':10})


    def parse(self, response):
        self.page +=1
        logger.error('> Pages loaded {}'.format(self.page))

        # Extracting product links on articles page
        urls = get_info.get_links(response)
        for url in urls:
            url = 'https://www.carrefour.fr' + url
            logger.error('> Rayon page - url : {}'.format(url))

            yield SplashRequest(url=url, callback=self.parse_article) #, args={'wait':5})


    def parse_article(self, response):
        self.object += 1
        logger.error('> Articles scrapped {}'.format(self.object))

        item = ArticleItem()

        logger.debug('staaart')

        item['description'] = get_info.get_description(response)
        item['description2'] = get_info.get_description2(response)
        item['titre'] = get_info.get_titre(response)
        item['soustitre'] = get_info.get_soustitre(response)
        item['similaire'] = get_info.get_similaire(response)
        item['price'] = get_info.get_price(response)
        logger.debug('ON EST ICI LES POTOS')
        # item['image_urls'] = get_info.get_picture_url(response)
        item['position'] = get_info.get_position(response)

        for key, value in item.items():
            logger.warn(key)
            logger.warn(value)
        yield item




