import scrapy
from scrapy.TA.spiders import get_info
from scrapy.TA import ReviewRestoItem

class QuotesSpider(scrapy.Spider):
    name = "restoTAcomment"

    def __init__(self, *args, **kwargs): 
        super(QuotesSpider, self).__init__(*args, **kwargs) 
        
        # Parse URL
        self.start_urls = [kwargs.get('start_url')] 
        if self.start_urls == [None]:
            self.start_urls =[
                'https://www.tripadvisor.co.uk/Restaurants-g191259-Greater_London_England.html' # zone
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse_review(self, response):
        
        comment_item = ReviewRestoItem()
        
        url =  get_info.get_review_url(response)
        id_comment = get_info.get_id_comment(url)
        comment_item['url'] = url
        comment_item['id_resto'] = get_info.get_id_resto(url)
        comment_item['id_comment'] = id_comment
        comment_item['resto'] =  get_info.get_resto_name(url)
        print('>>> Comment : {}'.format(id_comment), '\n', url)

        review = get_info.get_review(response)
        comment_item['resto_url'] = get_info.get_resto_url_from_review(review)
        comment_item['rating'] = get_info.get_review_rating(response)

        comment_item['title'] = get_info.get_review_title(review)
        comment_item['content'] = get_info.get_review_content(review)

        comment_item['diner_date'] = get_info.get_review_diner_date(review)
        comment_item['rating_date'] = get_info.get_review_rating_date(review)
        comment_item['answer_text'] = get_info.get_review_answer_text(review)

        comment_item['reviewer_pseudo'] = get_info.get_reviewer_pseudo_from_review(review)
        comment_item['reviewer_origin'] = get_info.get_reviewer_origin_from_review(review)
        comment_item['reviewer_info_sup'] =  get_info.get_reviewer_info_sup_from_review(review)
        #reviewer_url = get_info.get_reviewer_url_from_review(reviewer_pseudo)

        comment_item['other_ratings_category'] = get_info.get_other_ratings_category_from_review(review)
        comment_item['other_ratings_value'] = get_info.get_other_ratings_value_from_review(review)

        yield comment_item 

    def parse_resto(self, response):
        print('>> New Resto')
        reviews = get_info.get_reviews(response)
        urls_review = get_info.get_list_of_review_url(reviews)
        
        for url_review in urls_review:
             yield response.follow(url=url_review, callback=self.parse_review)

        #self.max_page = 10
        next_page, next_page_number = get_info.get_next_list_of_reviews(response)
        
        if get_info.go_to_next_page(next_page, next_page_number, self.max_page):
            yield response.follow(next_page, callback=self.parse_resto)

    def parse(self, response):
        print('>>> NEW PAGE OF RESTO')
        my_urls = get_info.get_list_of_resto_url(response)
        
        for urls in my_urls:
            print('>BOOM', urls)
            yield response.follow(url=urls, callback=self.parse_resto)

        #self.max_page = 2 # ATTENTION LE NET PAGE NUMBER FAIT 1 2 3 2 3 4 ... (2 page de trop chargées => Corriger le selector)
        next_page, next_page_number = get_info.get_next_list_of_resto(response)
        
        if get_info.go_to_next_page(next_page, next_page_number, self.max_page):
            yield response.follow(next_page, callback=self.parse)


