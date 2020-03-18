import scrapy
from TA.spiders import get_info
from TA.items import RestoItem

import logging
import logzero
from logzero import logger


class restoTAinfo(scrapy.Spider):
    name = "restoTAinfo"

    def __init__(self, *args, **kwargs):
        super(restoTAinfo, self).__init__(*args, **kwargs)

        # Set logging level
        logzero.loglevel(logging.DEBUG)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:
            self.start_urls = [
                # scrapy shell https://www.tripadvisor.fr/Restaurants-g187070-France.html
                # css = 'div.geo_name a ::attr(href)' 
                #
                # 'https://www.tripadvisor.co.uk/Restaurants-g191259-Greater_London_England.html'  # zone
                'https://www.tripadvisor.fr/Restaurants-g187265-Lyon_Rhone_Auvergne_Rhone_Alpes.html',
                'https://www.tripadvisor.fr/Restaurants-g187079-Bordeaux_Gironde_Nouvelle_Aquitaine.html',
                'https://www.tripadvisor.fr/Restaurants-g187139-Corsica.html',
                'https://www.tripadvisor.fr/Restaurants-g187253-Marseille_Bouches_du_Rhone_Provence_Alpes_Cote_d_Azur.html',
                'https://www.tripadvisor.fr/Restaurants-g187175-Toulouse_Haute_Garonne_Occitanie.html',
                'https://www.tripadvisor.fr/Restaurants-g187234-Nice_French_Riviera_Cote_d_Azur_Provence_Alpes_Cote_d_Azur.html',
                'https://www.tripadvisor.fr/Restaurants-g187178-Lille_Nord_Hauts_de_France.html',
                'https://www.tripadvisor.fr/Restaurants-g187075-Strasbourg_Bas_Rhin_Grand_Est.html',
                'https://www.tripadvisor.fr/Restaurants-g187153-Montpellier_Herault_Occitanie.html',
                'https://www.tripadvisor.fr/Restaurants-g187198-Nantes_Loire_Atlantique_Pays_de_la_Loire.html',
                'https://www.tripadvisor.fr/Restaurants-g187264-Grenoble_Isere_Auvergne_Rhone_Alpes.html',
                'https://www.tripadvisor.fr/Restaurants-g187209-Aix_en_Provence_Bouches_du_Rhone_Provence_Alpes_Cote_d_Azur.html',
                'https://www.tripadvisor.fr/Restaurants-g187103-Rennes_Ille_et_Vilaine_Brittany.html',
                'https://www.tripadvisor.fr/Restaurants-g187221-Cannes_French_Riviera_Cote_d_Azur_Provence_Alpes_Cote_d_Azur.html',
                'https://www.tripadvisor.fr/Restaurants-g187191-Rouen_Seine_Maritime_Haute_Normandie_Normandy.html',
                'https://www.tripadvisor.fr/Restaurants-g187212-Avignon_Vaucluse_Provence_Alpes_Cote_d_Azur.html',
                'https://www.tripadvisor.fr/Restaurants-g187130-Tours_Indre_et_Loire_Centre_Val_de_Loire.html',
                'https://www.tripadvisor.fr/Restaurants-g187091-Clermont_Ferrand_Puy_de_Dome_Auvergne_Rhone_Alpes.html',
                'https://www.tripadvisor.fr/Restaurants-g187111-Dijon_Cote_d_Or_Bourgogne_Franche_Comte.html'
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

        # To track the evolution of scrapping
        self.main_nb = 0
        self.resto_nb = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """MAIN PARSING : Start from a classical restaurant page
            - Usually there are 30 restaurants per page
        """
        logger.warn('> PARSING NEW MAIN PAGE OF RESTO ({})'.format(self.main_nb))

        self.main_nb += 1

        # Get the list of these 30 restaurants
        my_urls = get_info.get_urls_resto_in_main_search_page(response)
        for urls in my_urls:
            yield response.follow(url=urls, callback=self.parse_resto)

        next_page, next_page_number = get_info.get_urls_next_list_of_restos(response)

        if get_info.go_to_next_page(next_page, next_page_number, self.max_page):
            yield response.follow(next_page, callback=self.parse)

    def parse_resto(self, response):
        """REAL PARSING : Open a specific page with restaurant description
            - Read these data and store them
        """
        self.resto_nb += 1

        # Intitiate storing object
        resto_item = RestoItem()

        # URL
        url = get_info.get_resto_url(response)
        name_url = get_info.get_resto_name_in_url_from_resto(url)
        resto_item['id'] = get_info.get_id_resto(url)
        logger.info('- Resto ({}): {}'.format(self.resto_nb, name_url))

        # General
        general = get_info.get_review_information_from_resto(response)
        resto_item['titre'] = get_info.get_title_from_resto(general)
        resto_item['rating'] = get_info.get_rating_from_resto(general)
        resto_item['nb_review'] = get_info.get_nb_review_from_resto(general)
        resto_item['street_adress'] = get_info.get_street_adress_from_resto(general)
        resto_item['locality'] = get_info.get_locality_from_resto(general)
        resto_item['country'] = get_info.get_country_from_resto(general)  # BUG ?
        resto_item['tel_number'] = get_info.get_tel_number_from_resto(general)  # BUG ?

        # Information sup
        info_1 = get_info.get_info_1(general)
        resto_item['info_1'] = info_1
        resto_item['info_2'] = get_info.get_info_2(general)
        resto_item['price_range'] = get_info.get_price_range(info_1)

        # Picture related
        resto_item['picture_number'] = get_info.get_picture_number(response)

        # Rating and reviews
        ratings = get_info.get_ratings_and_reviews(response)
        resto_item['avg_rating'] = get_info.get_resto_avg_rating(ratings)
        resto_item['nb_reviews'] = get_info.get_resto_nb_review(ratings)
        resto_item['local_ranking'] = get_info.get_resto_local_ranking(ratings)
        resto_item['other_information'] = get_info.get_resto_other_information(ratings)
        resto_item['all_rankings'] = get_info.get_resto_all_rankings(ratings)  # BUG ?
        resto_item['categories_ranking'] = get_info.get_resto_categories_ranking(ratings)

        # Details
        rep = get_info.get_description_from_resto(response)
        resto_item['description'] = rep[0]
        resto_item['details'] = rep[1]

        # Reviews
        traveler_ratings = get_info.get_traveler_ratings_from_resto(response)
        resto_item['rating_excellent'] = traveler_ratings[0]
        resto_item['rating_very_good'] = traveler_ratings[1]
        resto_item['rating_average'] = traveler_ratings[2]
        resto_item['rating_poor'] = traveler_ratings[3]
        resto_item['rating_terrible'] = traveler_ratings[4]

        resto_item['name_url'] = name_url
        resto_item['url'] = url
        resto_item['url_menu'] = get_info.get_url_menu_from_resto(general)

        # Location and contact
        # Food and ambiance
        # Top 3 reasons to eat there

        yield resto_item
