################################################################################################
################################################################################################
#                                       Main functions
################################################################################################
################################################################################################

# ************************        NO NOT CHANGE THIS FUNCTION        ***************************


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


# ************************        ADAPAT ALL THOSE FUNCTIONS        ****************************


def get_article_urls(response):
    css_locator = '' 
    urls = response.css(css_locator).extract()
    return urls

def get_next_page_of_articles(response):
    css_locator = '' 
    next_page = response.css(css_locator).extract_first()
    return next_page

def get_next_page_number(next_page):
    next_page_number = next_page    # apply string manipulation to extract the number
    return next_page_number



################################################################################################
################################################################################################
#                                       Parsing a single referenec
################################################################################################
################################################################################################

# ************************        ADAPAT ALL THOSE FUNCTIONS        ****************************


def get_field_1(response):
    xpath = ''
    field_1 = response.xpath(xpath).extract_first()
    return field_1
   
def get_field_2(response):
    xpath = ''
    field_2 = response.xpath(xpath).extract_first()
    return field_2
   
def get_field_3(response):
    xpath = ''
    field_3 = response.xpath(xpath).extract_first()
    return field_3
   