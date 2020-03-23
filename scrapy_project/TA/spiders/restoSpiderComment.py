import scrapy
from TA.spiders import get_info
from TA.items import ReviewRestoItem
import logging
import logzero
from logzero import logger


class QuotesSpider(scrapy.Spider):
    name = "restoTAreview"

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)

        # Set logging level
        logzero.loglevel(logging.WARNING)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:
            self.start_urls = [
                # 'https://www.tripadvisor.co.uk/Restaurants-g191259-Greater_London_England.html'  # zone
                # 'https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html',
                # 'https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html',
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

        # self.max_resto_page = 50
        # self.max_review_page = 10
        self.max_resto_page = None
        self.max_review_page = None

        # To track the evolution of scrapping
        self.main_nb = 0
        self.resto_nb = 0
        self.review_nb = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """MAIN PARSING : Start from a classical reastaurant page
            - Usually there are 30 restaurants per page
        """
        logger.warn(' > PARSING NEW MAIN PAGE OF RESTO ({})'.format(self.main_nb))

        self.main_nb += 1

        # Get the list of these 30 restaurants
        my_urls = get_info.get_urls_resto_in_main_search_page(response)

        # For each url : dive into the restaurant to get the reveiws
        for url in my_urls:
            logger.warn('> New restaurant detected : {}'.format(url))
            yield response.follow(url=url, callback=self.parse_resto)

        # self.max_page = 2
        next_page, next_page_number = get_info.get_urls_next_list_of_restos(response)

        if get_info.go_to_next_page(next_page, next_page_number, self.max_resto_page):
            yield response.follow(next_page, callback=self.parse)

    def parse_resto(self, response):
        """SECOND PARSING : Given a restaurant, get each review url and get to parse it
            - Usually there are 10 comments per page
        """

        # Display a message into the console
        logger.warn(' > PARSING NEW RESTO PAGE ({})'.format(self.resto_nb))
        self.resto_nb += 1

        # Get the list of these 10 comments
        reviews = get_info.get_reviews_list_in_restaurant_page(response)
        urls_review = get_info.get_urls_reviews_in_restaurant_page(reviews)

        for url_review in urls_review:
            yield response.follow(url=url_review, callback=self.parse_review)

        next_page, next_page_number = get_info.get_urls_next_list_of_reviews(response)

        if get_info.go_to_next_page(next_page, next_page_number, self.max_review_page):
            yield response.follow(next_page, callback=self.parse_resto)

    def parse_review(self, response):
        """FINAL PARSING : Open a specific page with comment and client specifications
            - Read these data and store them
        """
        self.review_nb += 1

        # Create review item
        comment_item = ReviewRestoItem()

        # And then get all the related information
        url = get_info.get_review_url(response)
        id_comment = get_info.get_id_comment(url)
        comment_item['id_resto'] = get_info.get_id_resto(url)
        comment_item['id_comment'] = id_comment
        comment_item['resto'] = get_info.get_resto_name(url)

        review = get_info.get_review(response)
        comment_item['resto_url'] = get_info.get_review_resto_url(response)
        comment_item['rating'] = get_info.get_review_rating(response)

        title = get_info.get_review_title(review)
        comment_item['title'] = title

        comment_item['diner_date'] = get_info.get_review_diner_date(review)
        comment_item['rating_date'] = get_info.get_review_rating_date(review)
        comment_item['answer_text'] = get_info.get_review_answer_text(review)

        reviewer_pseudo = get_info.get_review_reviewer_pseudo(review)
        comment_item['reviewer_pseudo'] = reviewer_pseudo
        comment_item['reviewer_origin'] = get_info.get_review_reviewer_origin(review)
        comment_item['reviewer_info_sup'] = get_info.get_review_reviewer_info_sup(review)
        # reviewer_url = get_info.get_review_reviewer_url(reviewer_pseudo) (#TODO in post treatment)

        comment_item['other_ratings_category'] = get_info.get_review_other_ratings_category(review)
        comment_item['other_ratings_value'] = get_info.get_review_other_ratings_value(review)

        # Long observations (placed at the end to facilitate json files lecture)
        comment_item['url'] = url
        comment_item['content'] = get_info.get_review_content(review)

        # Displaying info in cmd
        logger.info('- Comment ({}): {} \t {}'.format(self.review_nb, id_comment, title))
        yield comment_item



