import scrapy
from TA.spiders import get_info


class QuotesSpider(scrapy.Spider):
    name = "restoTAinfo"

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:
            self.start_urls = [
                'https://www.tripadvisor.co.uk/Restaurants-g191259-Greater_London_England.html'  # zone
            ]
        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_resto(self, response):
        resto_item = ReviewRestoItem()

        # URL
        url = get_info.get_resto_url(response)
        name_url = get_info.get_resto_name_in_url_from_resto(url)
        resto_item['url'] = url
        resto_item['id'] = get_info.get_id_resto(url)
        resto_item['name_url'] = name_url
        print('> Parsing resto', name_url, '\n> ', url)

        # General
        general = get_info.get_review_information_from_resto_list(response)
        resto_item['titre'] = get_info.get_title_from_resto_list(general)
        resto_item['rating'] = get_info.get_rating_from_resto_list(general)
        resto_item['nb_review'] = get_info.get_nb_review_from_resto_list(general)
        resto_item['street_adress'] = get_info.get_street_adress_from_resto_list(general)
        resto_item['locality'] = get_info.get_locality_from_resto_list(general)
        resto_item['country'] = get_info.get_country_from_resto_list(general)
        resto_item['tel_number'] = get_info.get_tel_number_from_resto_list(general)
        resto_item['url_menu'] = get_info.get_url_menu_from_resto_list(general)

        resto_item['info_1'] = get_info.get_info_1(general)
        resto_item['info_2'] = get_info.get_info_2(general)
        resto_item['price_range'] = get_info.get_price_range(info_1)

        resto_item['picture_number'] = get_info.get_picture_number(response)

        # Rating and reviews
        resto_item['r_and_r'] = response.css('div.restaurants-detail-overview-cards-DetailOverviewCards__wrapperDiv--1Dfhf')
        resto_item['avg_rating'] = r_and_r.css('span.restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl::text').extract_first()
        resto_item['nb_reviews'] = r_and_r.css('a.restaurants-detail-overview-cards-RatingsOverviewCard__ratingCount--DFxkG::text').extract_first()
        resto_item['local_ranking'] = r_and_r.css('div.restaurants-detail-overview-cards-RatingsOverviewCard__ranking--17CmN ::text').extract()        
        resto_item['other_information'] = r_and_r.css('div.restaurants-detail-overview-cards-RatingsOverviewCard__award--31yzt ::text').extract()
        resto_item['all_rankings'] = r_and_r.css('span.ui_bubble_rating ::attr(class)').extract()[1:]
        resto_item['categories_ranking'] = r_and_r.css('span.restaurants-detail-overview-cards-RatingsOverviewCard__ratingText--1P1Lq ::text').extract()

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

        # Location and contact
        # Food and ambience
        # Top 3 reasons to eat there

        yield resto_item 


    def parse(self, response):
        
        my_urls = get_info.get_list_of_resto_url(response)
        for urls in my_urls:
            yield response.follow(url=urls, callback=self.parse_resto)

        next_page, next_page_number = get_info.get_next_list_of_resto(response)
        
        if get_info.go_to_next_page(next_page, next_page_number, self.max_page):
            yield response.follow(next_page, callback=self.parse)

