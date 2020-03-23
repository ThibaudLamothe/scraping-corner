# Scraping imports
import time
import scrapy
from logzero import logger
from TA.spiders import get_info


#############################################################################
#############################################################################
#############################################################################


# class SpiderAmazonTestingMain(scrapy.Spider):
#     name = "SpiderAmazonTestingMain"

#     def start_requests(self):
#         url = 'http://amazon.com/s?i=sporting-intl-ship&rh=n%3A%2116225014011&page=2&qid=1581438225&ref=lp_16225014011_pg_2'
#         yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         logger.error('--- STARTING MAIN UNIT TESTING ---')
        
#         # Get the url of each reference on the current page
#         links = get_info.get_reference_links(response)
#         logger.info(len(links))
#         logger.info(links[0])
#         assert len(links) == 24,                                            'get_info.get_reference_links -- links'


#         # Get pagination information
#         next_page, page_number = get_info.get_main_pagination(response)
#         logger.info('Next page : {}'.format(next_page))
#         logger.info('Page number : {}'.format(page_number))
#         assert type(next_page) == str,                                      'get_info.get_main_pagination -- next page'
#         assert '/s?i=sporting-intl-ship&rh=n%3A16225014011&' in next_page,  'get_info.get_main_pagination -- next page'
#         assert page_number == 2,                                            'get_info.get_main_pagination --  page number'
        
#         logger.error('--- MAIN UNIT TESTING IS OK ---')
#         time.sleep(3)
      

#############################################################################
#############################################################################
#############################################################################

class TAReviewSpiderTest(scrapy.Spider):
    name = "restoTAreviewTesting"
    
       
    def start_requests(self):
    
        # Testing main (1/2)
        url = 'https://www.tripadvisor.fr/Restaurants-g187079-Bordeaux_Gironde_Nouvelle_Aquitaine.html'
        yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(test=1))

        # Testing main (2/2)   
        url = 'https://www.tripadvisor.fr/Restaurants-g187079-oa30-Bordeaux_Gironde_Nouvelle_Aquitaine.html#EATERY_LIST_CONTENTS'
        yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(test=2))

        # Testing resto
        # url = 'https://www.tripadvisor.fr/Restaurant_Review-g187079-d1194787-Reviews-or40-Julien_Cruege-Bordeaux_Gironde_Nouvelle_Aquitaine.html'
        url = 'https://www.tripadvisor.fr/Restaurant_Review-g187079-d1194787-Reviews-Julien_Cruege-Bordeaux_Gironde_Nouvelle_Aquitaine.html'
        yield scrapy.Request(url=url, callback=self.parse_resto)

        # Testing reveiw
        url = 'https://www.tripadvisor.fr/ShowUserReviews-g187079-d1194787-r746278889-Julien_Cruege-Bordeaux_Gironde_Nouvelle_Aquitaine.html'
        yield scrapy.Request(url=url, callback=self.parse_review)


    def parse(self, response, test=0):
        """MAIN PARSING : Start from a classical reastaurant page
            - Usually there are 30 restaurants per page
        """
        logger.error('--- STARTING MAIN ({}) UNIT TESTING ---'.format(test))
        
        # Get the list of these 30 restaurants
        my_urls = get_info.get_urls_resto_in_main_search_page(response)
        urls_start = [True if url.startswith('/Restaurant_Review-') else False for url in my_urls]
        assert len(my_urls)==37
        assert sum(urls_start)==37
        
        next_page, next_page_number = get_info.get_urls_next_list_of_restos(response)
        logger.debug(next_page)
        logger.debug(next_page_number)    
        if test==1:
            assert int(next_page_number)==2
        if test==2:
            assert int(next_page_number)==3
        
        logger.error('--- MAIN ({}) UNIT TESTING IS FINISHED ---'.format(test))
        time.sleep(3)

        
    def parse_resto(self, response):
        """SECOND PARSING : Given a restaurant, get each review url and get to parse it
            - Usually there are 10 comments per page
        """
        logger.error('--- STARTING RESTAURANT UNIT TESTING ---')
        
        # Get the list of these 10 comments
        reviews = get_info.get_reviews_list_in_restaurant_page(response)
        urls_review = get_info.get_urls_reviews_in_restaurant_page(reviews)
        urls_start = [True if url.startswith('/ShowUserReviews-') else False for url in urls_review]
        logger.debug(len(reviews))
        logger.debug(urls_review[0])
        assert len(reviews)==10
        assert len(urls_review)==10
        assert sum(urls_start)==10
        
        
        next_page, next_page_number = get_info.get_urls_next_list_of_reviews(response)
        logger.debug(next_page)
        logger.debug(next_page_number)

        logger.error('--- RESTAURANT UNIT TESTING IS FINISHED ---')
        time.sleep(3)


    def parse_review(self, response):
        """FINAL PARSING : Open a specific page with comment and client specifications
            - Read these data and store them
        """
        logger.error('--- STARTING REVIEW UNIT TESTING ---')
        
        # # And then get all the related information
        # url = get_info.get_review_url(response)
        # id_comment = get_info.get_id_comment(url)
        # comment_item['id_resto'] = get_info.get_id_resto(url)
        # comment_item['id_comment'] = id_comment
        # comment_item['resto'] = get_info.get_resto_name(url)

        # review = get_info.get_review(response)
        # comment_item['resto_url'] = get_info.get_review_resto_url(response)
        # comment_item['rating'] = get_info.get_review_rating(response)

        # title = get_info.get_review_title(review)
        # comment_item['title'] = title

        # comment_item['diner_date'] = get_info.get_review_diner_date(review)
        # comment_item['rating_date'] = get_info.get_review_rating_date(review)
        # comment_item['answer_text'] = get_info.get_review_answer_text(review)

        # reviewer_pseudo = get_info.get_review_reviewer_pseudo(review)
        # comment_item['reviewer_pseudo'] = reviewer_pseudo
        # comment_item['reviewer_origin'] = get_info.get_review_reviewer_origin(review)
        # comment_item['reviewer_info_sup'] = get_info.get_review_reviewer_info_sup(review)
        # # reviewer_url = get_info.get_review_reviewer_url(reviewer_pseudo) (#TODO in post treatment)

        # comment_item['other_ratings_category'] = get_info.get_review_other_ratings_category(review)
        # comment_item['other_ratings_value'] = get_info.get_review_other_ratings_value(review)

        # # Long observations (placed at the end to facilitate json files lecture)
        # comment_item['url'] = url
        # comment_item['content'] = get_info.get_review_content(review)
        
        logger.error('--- REVIEW UNIT TESTING IS OK ---')
        time.sleep(3)


