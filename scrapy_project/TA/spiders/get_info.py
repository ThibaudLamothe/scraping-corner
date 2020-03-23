################################################################################################
#                              DECIDING IF GOING TO NEXT PAGE OR NOT 
################################################################################################


def go_to_next_page(next_page, next_page_number, max_page, printing=False):
    if next_page is None:
        if printing: print(' - There is no next_page')
    else:
        if printing: print(' - There is a next_page')
        if printing: print(' - Page url is : {}'.format(next_page))
        if max_page is None:
            if printing: print(' - There is no number of page restriction. Go on.')
            # yield response.follow(next_page, callback=self.parse_resto)
            return True
        else:
            if printing: print(' - Max page number is : {}'.format(max_page))

            if next_page_number is None:
                if printing: print(' -  No next number page : STOP.')
            else:
                if printing: print(' - Next page number is {}'.format(next_page_number))
                if int(next_page_number) <= int(max_page):
                    if printing: print(' - It is smaller than limit. Go on.')
                    # yield response.follow(next_page, callback=self.parse_resto)
                    return True
                else:
                    if printing: print('LIMIT was reached. STOP.')
    return False


################################################################################################
################################################################################################
#                                       TA NAVIGATION 
################################################################################################
################################################################################################

def get_urls_resto_in_main_search_page(response):
    #return response.css('a.restaurants-list-ListCell__restaurantName--2aSdo ::attr(href)').extract()
    urls = response.xpath('//*[@class="_15_ydu6b"]').css('::attr(href)').extract()
    #urls = [url for url in urls if '.' in url[:5]]
    return urls


def get_urls_reviews_in_restaurant_page(reviews):
    return reviews.css('div.quote a ::attr(href)').extract()


def get_urls_next_list_of_restos(response):
    xpath = '//*[@id="EATERY_LIST_CONTENTS"]/div/div/a'
    next_page = response.xpath(xpath).css('::attr(href)').extract()[-1]
    next_page_number = response.xpath(xpath).css('::attr(data-page-number)').extract()[-1]
    return next_page, next_page_number


def get_urls_next_list_of_reviews(response):
    # xpath = '//a[@class="nav next ui_button primary"]'
    xpath = '//div[@class="unified ui_pagination "]/a[contains(@class,"nav next")]'
    next_page = response.xpath(xpath).css('::attr(href)').extract_first()
    next_page_number = response.xpath(xpath).css('::attr(data-page-number)').extract_first()
    return next_page, next_page_number


################################################################################################
################################################################################################
#                                       REVIEW INFORMATION 
################################################################################################
################################################################################################

######################
#  Caclulation Part  #
######################

def get_review_url(response):
    return response.url


def get_id_resto(url):
    return url.split('-')[1] + '-' + url.split('-')[2]


def get_id_comment(url):
    id_resto = get_id_resto(url)
    return id_resto + '-' + url.split('-')[3]


def get_resto_name(url):
    return url.split('-')[4]


def get_review_reviewer_url(reviewer_pseudo):
    return 'https://www.tripadvisor.co.uk/Profile/{}'.format(reviewer_pseudo)


######################
#  Scrapping Part    #
######################

def get_reviews_list_in_restaurant_page(response):
    return response.css('div.review-container')


def get_review(response):
    return response.css('div.review-container')[0]


def get_review_resto_url(response):
    return response.css('div.surContent a.HEADING::attr(href)').extract_first()


def get_review_rating(response):
    return response.css('div.rating span span::attr(alt)').extract_first().split(' ')[0]


def get_review_title(review):
    return review.css('div.quote a span.noQuotes ::text').extract_first()


def get_review_content(review):
    return review.css('div.entry')[0].css('p.partial_entry::text').extract()


def get_review_diner_date(review):
    try:
        diner_date = review.css('div.prw_reviews_stay_date_hsx ::text').extract()[-1]
    except:
        print('> ERROR : diner_date')
        diner_date = None
    return diner_date


def get_review_rating_date(review):
    try:
        rating_date = review.css('span.ratingDate::attr(title)').extract_first()
    except:
        print('> ERROR : rating_date')
        rating_date = None
    return rating_date


def get_review_answer_text(review):
    has_answer = False
    answer_text = None
    if len(review.css('div.entry')) > 1:
        has_answer = True
        answer_text = review.css('div.entry')[1].css('p.partial_entry::text').extract()
    return answer_text


def get_review_reviewer_pseudo(review):
    try:
        reviewer_pseudo = review.css('span.scrname::text').extract_first()
    except:
        reviewer_pseudo = None
    return reviewer_pseudo


def get_review_reviewer_origin(review):
    try:
        reviewer_origin = review.css('span.userLocation::text').extract()
    except:
        reviewer_origin = None
    return reviewer_origin


def get_review_reviewer_info_sup(review):
    try:
        info = review.css('div.memberBadgingNoText span ::attr(class)').extract()
        info = [i.replace('ui_icon ', '') for i in info if i != 'badgetext']
        count = review.css('span.badgetext::text').extract()
        reviewer_info_sup = list(zip(info, count))
    except:
        reviewer_info_sup = None
    return reviewer_info_sup


def get_review_other_ratings_category(review):
    try:
        other_ratings_category = review.css('li.recommend-answer ::text').extract()
    except:
        other_ratings_category = None
    return other_ratings_category


def get_review_other_ratings_value(review):
    try:
        other_ratings_value = review.css('li.recommend-answer div.ui_bubble_rating::attr(class)').extract()
        other_ratings_value = [i.split('_')[-1] for i in other_ratings_value]
    except:
        other_ratings_value = None
    return other_ratings_value


################################################################################################
################################################################################################
#                                       RESTO INFORMATION 
################################################################################################
################################################################################################


######################
#  Caclulation Part  #
######################

# url
def get_resto_url(response):
    return response.url


def get_resto_name_in_url_from_resto(url):
    return url.split('-')[-2]


######################
#  Scrapping Part    #
######################

def get_review_information_from_resto(response):
    return response.xpath('//*[@id="taplc_resp_rr_top_info_rr_resp_0"]/div')


# General
def get_title_from_resto(general):
    return general.css('h1::text').extract_first()


def get_rating_from_resto(general):
    try:
        return general.css('div.ratingContainer div span::attr(alt)').extract_first().split(' ')[0]
    except:
        print('> Error with RATING')
        return None


def get_nb_review_from_resto(general):
    nb_review = general.css('div.ratingContainer span.reviewCount::text').extract_first()
    if nb_review:
        return nb_review.split(' ')[0]
    return 0


def get_street_adress_from_resto(general):
    return general.css('span.street-address::text').extract()


def get_locality_from_resto(general):
    return general.css('span.locality::text').extract()


def get_country_from_resto(general):
    try:
        country = general.css('span.detail::text').extract()[1] 
    except:
        country = None
        print(' > Error with COUNTRY')
    return country


def get_tel_number_from_resto(general):
    try:
        tel_number = general.css('span.detail::text').extract()[2]
        tel_number2 = general.css('span.is-hidden-mobile::text').extract_first()
    except:
        tel_number = None
        tel_number2 = None
        print('> Error with TEL Number')
    return tel_number


def get_url_menu_from_resto(general):
    return general.css('div.is-hidden-mobile::attr(onclick)').extract()[-1].split('\'')[-2]


def get_traveler_ratings_from_resto(response):
    return response.css('div.content div.choices span.row_num ::text').extract()


def get_info_1(general):
    try:
        info_1 = general.css('div.header_links a::text').extract()
    except:
        info_1 = None
    return info_1


def get_info_2(general):
    try:
        info_2 = general.css('div.header_links::text').extract()
    except:
        info_2 = None
    return info_2


def get_price_range(info_1):
    try:
        price_range = info_1[0]
    except:
        price_range = None
    return price_range


def get_picture_number(response):
    try:
        picture_number = response.css('span.see_all_count span.details::text').extract_first().split(' ')[-1][1:-1]
    except:
        picture_number = None
    return picture_number


def get_description_from_resto(response):
    details = response.css('div.restaurants-details-card-DetailsCard__innerDiv--1Imq5')
    long_description = details.css(
        'div.restaurants-details-card-DesktopView__desktopAboutText--1VvQH::text').extract_first()
    details = details.css('div.ui_column ::text').extract()
    return long_description, details


# Rating and reviews
def get_ratings_and_reviews(response):
    return response.css('div.restaurants-detail-overview-cards-DetailOverviewCards__wrapperDiv--1Dfhf')


def get_resto_avg_rating(rating):
    return rating.css(
        'span.restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl::text').extract_first()


def get_resto_nb_review(rating):
    return rating.css(
        'a.restaurants-detail-overview-cards-RatingsOverviewCard__ratingCount--DFxkG::text').extract_first()


def get_resto_local_ranking(rating):
    return rating.css('div.restaurants-detail-overview-cards-RatingsOverviewCard__ranking--17CmN ::text').extract()


def get_resto_other_information(rating):
    return rating.css('div.restaurants-detail-overview-cards-RatingsOverviewCard__award--31yzt ::text').extract()


def get_resto_all_rankings(rating):
    return rating.css('span.ui_bubble_rating ::attr(class)').extract()[1:]


def get_resto_categories_ranking(rating):
    return rating.css('span.restaurants-detail-overview-cards-RatingsOverviewCard__ratingText--1P1Lq ::text').extract()