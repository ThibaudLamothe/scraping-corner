#############################################################################
#############################################################################
#############################################################################

# General import
import datetime

# Scraping imports
import scrapy
from LBC.items import LBCShortItem, LBCAnnonceItem
from LBC.spiders import get_info

# Logging import
import logzero
import logging
from logzero import logger

logzero.loglevel(logging.DEBUG) # To display content information
# logzero.loglevel(logging.INFO)  # To see number of parsed references
# logzero.loglevel(logging.WARN)  # To see number of parsed main pages

#############################################################################
#############################################################################
#############################################################################

class SpiderLBC(scrapy.Spider):
    name = "spiderLBC"

    def __init__(self, *args, **kwargs):
        super(SpiderLBC, self).__init__(*args, **kwargs)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:
            self.start_urls = [
                'https://www.leboncoin.fr/recherche/?category=9&locations=Nantes,Rennes,Reims_51100,Bordeaux,Talence_33400,Pessac_33600,M%C3%A9rignac_33700&real_estate_type=2&immo_sell_type=old&price=75000-125000'
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)
        else:
            self.max_page = 1

        # Scrapping compteur
        self.page = 0
        self.object = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_main)
            # yield scrapy.Request(url=url, callback=self.parse_short_annonce)


#############################################################################
#############################################################################
#############################################################################

    def parse_main(self, response):
        
        # Number of main page scrapped
        self.page += 1
        logger.warn('Parse page ({}) - object ({})'.format(self.page, self.object))

        # Get the url of each page
        lbc_items = get_info.get_items(response)
        links = [get_info.get_url_main(lbc_item) for lbc_item in lbc_items]
        
        # Following links
        for link in links:
            yield response.follow(url=link, callback=self.parse_annonce)

        # Following next page
        next_page, next_page_number = get_info.get_next_list_of_announces(response)
        if get_info.go_to_next_page(next_page, next_page_number, self.max_page):
            yield response.follow(next_page, callback=self.parse_main)
        

    def parse_annonce(self, response):

        # Displaying quantity information
        self.object += 1
        logger.info('Parse object ({})'.format(self.object))

        # Creating annonce item
        item = LBCAnnonceItem()

        # Identification of annonce
        id_ = get_info.get_id(response)
        logger.debug('Parsing annonce : {}'.format(id_))

        # Basic information
        item['id_'] = id_
        item['url'] = response.url
        item['titre'] = get_info.get_titre(response)
        item['description'] = get_info.get_description(response)
        item['prix'] = get_info.get_prix(response)
        item['date_absolue'] = get_info.get_date(response)
        item['auteur'] = get_info.get_auteur(response)

        # About sale location
        localisation = get_info.get_localisation(response)
        item['ville'] = localisation[0]
        item['code_postal'] = localisation[-1]

        # Is there any contact
        buttons = get_info.get_buttons(response)
        is_numero, is_envoi_msg = get_info.check_buttons(buttons)
        item['is_msg'] = is_envoi_msg
        item['is_num'] = is_numero

        criteres = get_info.get_criteres(response)
        criteres_dict = get_info.critere_cleaning(criteres)
        item['critere'] = criteres_dict
        logger.debug('Criteres : {}'.format(len(criteres_dict.keys())))
        
        nb_pict = 3  # self.results[id_]['nb_pict']
        categorie = 'cat'  # self.results[id_]['categorie']
        item['nb_pict'] = nb_pict
        item['categorie'] = categorie

        yield item


#############################################################################
#############################################################################
#############################################################################

    def parse_short_annonce(self, response):

        # Number of main page scrapped
        self.page += 1
        logger.warn('Parse page ({})'.format(self.page))

        # Get the url of each page
        lbc_items = get_info.get_items(response)
        logger.debug('> Found {} items.'.format(len(lbc_items)))

        for lbc_item in lbc_items:
            
            # Get information from main page
            lbc_item = get_info.get_item(lbc_item)
            titre = get_info.get_titre_main(lbc_item)
            url = get_info.get_url_main(lbc_item)

            item = LBCShortItem

            item['titre']= titre,
            item['url']= url,
            item['prix']= get_info.get_prix_main(lbc_item),
            item['categorie']=get_info.get_categorie_main(lbc_item),
            item['lieu']=get_info.get_lieu_main(lbc_item),
            item['date']= get_info.get_date_main(lbc_item),
            item['nb_pict']= get_info.get_nb_pict_main(lbc_item)
            
            logger.debug('> Parsing : {} on main page'.format(titre))
            logger.debug('> Results found : ', list(item.keys()))
            yield item

        # Following next page
        next_page, next_page_number = get_info.get_next_list_of_announces(response)
        if get_info.go_to_next_page(next_page, next_page_number, self.max_page):
            yield response.follow(next_page, callback=self.parse_short_annonce)
