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
            #yield response.follow(next_page, callback=self.parse_resto)
            return True
        else:
            if printing: print(' - Max page number is : {}'.format(max_page))

            if next_page_number is None:
                if printing: print(' -  No next number page : STOP.')
            else:
                if printing: print(' - Next page number is {}'.format(next_page_number))
                if int(next_page_number) <= int(max_page):
                    if printing: print(' - It is smaller than limit. Go on.')
                    #yield response.follow(next_page, callback=self.parse_resto)
                    return True
                else:
                    if printing: print('LIMIT was reached. STOP.')
    return False


def isin_rep(rep, val='p'):

    p = [i for i in rep if val in i ]
    if len(p) ==1:
        p = p[0].split(' ')[0]
    else:
        p = None
    return p


################################################################################################
################################################################################################
#                                       Parsing main
################################################################################################
################################################################################################

def get_items(response):
    return response.css('div.ergov3-annonce')


def get_prix(pv_item):
    return pv_item.css('div.ergov3-priceannonce::text').extract()[1].split('\n')[1].split('€')[0]


def get_titre(pv_item):
    # titre = pv_item.css('a.voirann::attr(title)').extract_first()
    return pv_item.css('div.ergov3-annonce a:nth-child(2)::attr(title)').extract_first()


def get_ville_cp(pv_item):
    return pv_item.css('div.ergov3-txtannonce cite').extract_first()


def get_nb_pict(pv_item):
    return pv_item.css('span.re14_nbphotos::text').extract_first()

def get_agence(pv_item):
    return pv_item.css('div.ergov3-bottomannonce div img::attr(alt)').extract_first()


def get_small_description(pv_item):
    return pv_item.css('div.ergov3-txtannonce p::text').extract()

def get_url(pv_item):
    return pv_item.css('a.voirann::attr(href)').extract_first()


def get_next_list_of_annonces(response):
    next_page = response.css('div.pv15-pagsuiv ::attr(href)').extract()[-1]
    next_page_number = int(next_page.split('&p=')[-1]) if len(next_page.split('&p=')) > 0 else None
    return next_page, next_page_number