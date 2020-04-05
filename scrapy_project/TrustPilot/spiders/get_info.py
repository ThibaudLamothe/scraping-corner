from logzero import logger
################################################################################################
################################################################################################
#                                       Main functions
################################################################################################
################################################################################################


def go_to_next_page(next_page, next_page_number, max_page, printing=False):
    if next_page is None:
        if printing: print(' - There is no next_page')
    else:
        if printing: print(' - There is a next_page')
        if printing: print(' - Page url is : {}'.format(next_page))
        if max_page is None:
            if printing: print(' - There is no number of page restriction. Go on.')
            return True
        else:
            if printing: print(' - Max page number is : {}'.format(max_page))

            if next_page_number is None:
                if printing: print(' -  No next number page : STOP.')
            else:
                if printing: print(' - Next page number is {}'.format(next_page_number))
                if int(next_page_number) <= int(max_page):
                    if printing: print(' - It is smaller than limit. Go on.')
                    return True
                else:
                    if printing: print('LIMIT was reached. STOP.')
    return False


################################################################################################
################################################################################################
#                                       Parsing main
################################################################################################
################################################################################################

def get_article_urls(response):
    css_locator = 'div.businessUnitCardsContainer___Qhix1 a ::attr(href)' 
    articles = response.css(css_locator).extract()
    urls = set(articles)
    return urls

def get_next_page_of_articles(response):
    try:
        # css_locator = 'h1 ::text'
        # next_page = response.css(css_locator).extract_first()
        
        
        # logger.info(xpath)
        # logger.info(next_age)
        # if next_page is None:
        xpath = '//a[@data-pagination-button-next-paginationlink="true"]/@href'
        logger.info(xpath)
        next_page = response.xpath(xpath).extract_first()
        logger.info(next_page)
        

        return next_page
    except:
        return None

# used for both articles and reviews's next pages
def get_next_page_number(next_page):
    try:
        next_page_number = next_page.split('&')
        next_page_number = [i for i in next_page_number if 'page=' in i]

        next_page_number = int(next_page_number[0].split('page=')[-1])
        return next_page_number
    except:
        return None

################################################################################################
################################################################################################
#                                       Parsing a single referenec
################################################################################################
################################################################################################

def get_next_page_of_reviews(response):
    try:
        xpath = '//a[@data-page-number="next-page"]/@href'
        next_page = response.xpath(xpath).extract_first()
        return next_page
    except:
        return None

def get_institute(response):
    try:
        # response.url.split('/')[-1]
        css = 'span.multi-size-header__big ::text'
        institute = response.css(css).extract_first()
        return institute
    except:
        return None

def get_reviews(response):
    css = 'div.review-card'
    reviews = response.css(css)
    return reviews

def get_review_auteur(review):
    css = 'div.consumer-information__name ::text'
    auteur = review.css(css).extract_first()
    return auteur

def get_nb_reviews_auteur(review):
    css = 'div.consumer-information__data span ::text'
    auteur_reviews = review.css(css).extract_first()
    return auteur_reviews

def get_review_rating(review):
    css = 'img ::attr(alt)'
    rating = review.css(css).extract_first()
    return rating

def get_review_title(review):
    css = 'h2.review-content__title > a ::text'
    title = review.css(css).extract_first()
    return title

def get_review_date(review):
    css = 'div.review-content-header__dates script ::text'
    date = review.css(css).extract_first()
    return date 

def get_review_content(review):
    css = 'p.review-content__text ::text'
    content = review.css(css).extract()
    return content 

def is_answers_to_review(review):
    css = 'div.review-stack ::attr(data-review-count)'
    is_multiple = review.css(css).extract_first()
    return is_multiple 

def get_review_url(review):
    css = 'h2.review-content__title > a ::attr(href)'
    url = review.css(css).extract_first()
    return url 