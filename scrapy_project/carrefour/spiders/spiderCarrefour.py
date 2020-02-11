import scrapy

import scrapy
# from scrapy_TA.spiders import get_info
# from scrapy_TA.items import RestoItem

import logging
import logzero
from logzero import logger

import time

class SpiderCarrefour(scrapy.Spider):
    name = "CarrefourSpider"


    def __init__(self, *args, **kwargs):
        super(SpiderCarrefour, self).__init__(*args, **kwargs)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:
            self.start_urls =[
                'https://www.carrefour.fr/'
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

        self.page = 0
        self.object = 0


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # view(response)


        css_selector = 'li.nav-item'
        rayons = response.css(css_selector)
        len(rayons)




        ####################################################
        ####################################################
        ####################################################
        ####################################################
        ####################################################

        # Getting rayons list
        liste = response.css('li.nav-item ::text').extract()
        logger.warn('List complete {}'.format(len(liste)))
        logger.warn('List complete {}'.format(liste))

        # Preaparong rayons fur sub analysis
        css_selector = 'li.nav-item'
        rayons = response.css(css_selector)
        logger.warn('Nb rayon {}'.format(len(rayons)))

        for rayon in rayons[2:4]:
            # Rayon information
            name = rayon.css(' ::text').extract()
            logger.warn('> rayon'.format(name))
            lien = rayon.css(' a ::attr(href)').extract()
            logger.warn('> lien'.format(lien))

            #  Try to eextract subrayon information
            # subrayon = rayon.css('ul > li.nav-item > a ::text').extract()


            yield response.follow(lien, callback=self.parse_rayon)
            # yield {'name': name, 'lien': lien, 'subrayon':subrayon}

        # filename = 'quotes-%s.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)




    def parse_rayon(self, response):
        logger.error('In here {}'.format(response.url))
        subrayon = response.css(' div.ds-carousel__item ::text').extract()
        yield {'subrayon':subrayon}



    def parse_sub_rayon(self, response):
        subrayon = response.css('div.ds-carousel__item ::text').extract()
        yield {'subrayon':subrayon}

    def parse_sub_sub_rayon(self, response):
        subrayon = response.css('div.ds-carousel__item ::text').extract()
        yield {'subrayon':subrayon}

    def parse_article(self, response):
        article = None
        yield article