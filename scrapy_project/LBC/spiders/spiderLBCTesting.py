# Scraping imports
import time
import scrapy
from logzero import logger
from LBC.spiders import get_info



#############################################################################
#############################################################################
#############################################################################


class spiderLBCTestingLong(scrapy.Spider):
    name = "spiderLBCTestingLong"

    def start_requests(self):
        url = 'https://www.leboncoin.fr/recherche/?category=9&locations=Nantes,Rennes,Reims_51100,Bordeaux,Talence_33400,Pessac_33600,M%C3%A9rignac_33700&real_estate_type=2&immo_sell_type=old&price=75000-125000'
        url = 'https://www.leboncoin.fr/recherche/?category=9&locations=Paris'
        yield scrapy.Request(url=url, callback=self.parse_main)
           
    def parse_main(self, response):
        
        logger.error('-'* 50)
        logger.error('-'* 50)
        logger.error('--- STARTING MAIN UNIT TESTING (1/2) ---')
        
        # Get items objects
        lbc_items = get_info.get_items(response)
        logger.debug('Nb links : {}'.format(len(lbc_items)))
        assert lbc_items is not None,                           'get_info.get_items'
        assert len(lbc_items)==35,                              'get_info.get_items'

        # Get links
        links = [get_info.get_url_main(lbc_item) for lbc_item in lbc_items]
        link = links[0]
        logger.debug('Nb links : {}'.format(len(links)))
        assert links is not None,                               'get_info.get_url_main'
        assert len(links)==len(lbc_items),                      'get_info.get_url_main'

        
        # Following next page
        next_page, next_page_number = get_info.get_next_list_of_announces(response)
        assert type(next_page) == str,                          'get_info.get_next_list_of_announces'
        assert '/recherche/?category=' in next_page,            'get_info.get_next_list_of_announces'
        assert next_page_number == 2,                           'get_info.get_next_list_of_announces'

        logger.error('--- MAIN UNIT TESTING IS OK (1/2) ---')
        time.sleep(3)

        yield response.follow(url=link, callback=self.parse_annonce)
        

    def parse_annonce(self, response):

        logger.error('--- STARTING ANNOUNCE UNIT TESTING ---')
        logger.warn(response.url)

        # Identification of annonce
        id_ = get_info.get_id(response)
        logger.debug(id_)
        assert int(id_[0]) in range(1,9)
        assert len(id_) in [10]
        
        # Basic information
        titre = get_info.get_titre(response)
        logger.debug(titre)
        assert type(titre) == str

        description = get_info.get_description(response)
        logger.debug(description)
        assert type(titre) == str

        prix = get_info.get_prix(response)
        logger.debug(prix)
        assert type(titre) == str

        date_absolue = get_info.get_date(response)
        logger.debug(date_absolue)
        assert type(titre) == str

        auteur = get_info.get_auteur(response)
        logger.debug(auteur)
        assert type(titre) == str

        # About sale location
        localisation = get_info.get_localisation(response)
        logger.debug(localisation)
        assert type(titre) == str

        ville = localisation[0]
        logger.debug(ville)
        assert type(titre) == str

        code_postal = localisation[-1]
        logger.debug(code_postal)
        assert type(titre) == str

        # Is there any contact
        buttons = get_info.get_buttons(response)
        is_numero, is_envoi_msg = get_info.check_buttons(buttons)
        logger.debug(is_numero)
        logger.debug(is_envoi_msg)
        assert type(titre) == str
        assert type(titre) == str
        
        criteres = get_info.get_criteres(response)
        logger.debug(criteres)
        assert type(titre) == str

        criteres_dict = get_info.critere_cleaning(criteres)
        logger.debug(criteres_dict)
        assert type(titre) == str
        
        logger.error('--- ANNOUNCE UNIT TESTING IS OK ---')
        time.sleep(3)


#############################################################################
#############################################################################
#############################################################################

class spiderLBCTestingShort(scrapy.Spider):
    name = "spiderLBCTestingShort"

    def start_requests(self):
        url = 'https://www.leboncoin.fr/recherche/?category=9&locations=Nantes,Rennes,Reims_51100,Bordeaux,Talence_33400,Pessac_33600,M%C3%A9rignac_33700&real_estate_type=2&immo_sell_type=old&price=75000-125000'
        yield scrapy.Request(url=url, callback=self.parse_short_annonce)


    def parse_short_annonce(self, response):
        
        logger.error('--- STARTING MAIN UNIT TESTING (2/2) ---')

        # Get the url of each page
        lbc_items = get_info.get_items(response)

        lbc_item = lbc_items[0]
            
        # Get information from main page
        lbc_item = get_info.get_item(lbc_item)
        titre = get_info.get_titre_main(lbc_item)
        url = get_info.get_url_main(lbc_item)
        prix = get_info.get_prix_main(lbc_item)
        categorie = get_info.get_categorie_main(lbc_item)
        lieu = get_info.get_lieu_main(lbc_item)
        date = get_info.get_date_main(lbc_item)
        nb_pict = get_info.get_nb_pict_main(lbc_item)
            
        # Following next page
        next_page, next_page_number = get_info.get_next_list_of_announces(response)

        logger.error('--- MAIN UNIT TESTING IS OK (2/2) ---')
        logger.error('-'*50)
        logger.error('-'*50)
        time.sleep(20)
