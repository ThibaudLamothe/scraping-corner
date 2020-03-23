################################################################################################
################################################################################################
#                                       Main functions
################################################################################################
################################################################################################
from logzero import logger


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


def is_url_already_in_db(url_id, id_list):
    logger.debug('> Checking if ID : {} already in db'.format(url_id))
    # print(id_list)
    id_list = [str(i) for i in id_list]
    logger.debug('  {}'.format(str(url_id) in id_list))
    return str(url_id) in id_list


def critere_cleaning(criteres):
    dict_crit = {}
    for crit in criteres.xpath('div'):
        extraction_crit = crit.css('::text').extract()
        critere_name = extraction_crit[0]
        critere_value = extraction_crit[1]
        # print('CRITERE : ', critere_name)
        if (critere_name == 'GES') or (
                critere_name == 'Classe énergie'):  # ('Classe' in critere_name and 'nergie' in critere_name) :
            # print('Specific criter')
            critere_value = 'NA'
        dict_crit[critere_name] = critere_value
    return dict_crit


def check_buttons(buttons):
    is_numero = False
    if 'Voir le numéro' in buttons:
        is_numero = True
    is_envoi_msg = False
    if 'Envoyer un message' in buttons:
        is_envoi_msg = True
    return is_numero, is_envoi_msg

################################################################################################
################################################################################################
#                                       Parsing main
################################################################################################
################################################################################################

def get_items(response):
    return response.css('li._3DFQ-')


def get_item(lbc_item):
    return lbc_item.xpath('.')


def get_titre_main(lbc_item):
    return lbc_item.css('p._2tubl span::text').extract_first()


def get_url_main(lbc_item):
    # url_id = url.split('/')[-2].split('.')[0]
    return lbc_item.css('a::attr(href)').extract_first()


def get_prix_main(lbc_item):
    return lbc_item.css('span._1NfL7::text').extract_first()


def get_categorie_main(lbc_item):
    return lbc_item.css('p.CZbT3::text').extract_first()


def get_lieu_main(lbc_item):
    return lbc_item.css('p._2qeuk::text').extract_first()


def get_date_main(lbc_item):
    return lbc_item.css('p.mAnae::text').extract_first()


def get_nb_pict_main(lbc_item):
    return lbc_item.css('span._2lY3w span:nth-of-type(2)::text').extract_first()


################################################################################################
################################################################################################
#                                       Parsing annonce
################################################################################################
################################################################################################

def get_id(response):
    return response.url.split('/')[-2].split('.')[0]

def get_titre(response):
    # titre =  response.css('h1._1KQme ::text').extract_first()
    # return response.css('h1._246DF ::text').extract_first()
    return response.css('h1.dgtty ::text').extract_first()

def get_description(response):
    return response.css('span.content-CxPmi ::text').extract()

def get_prix(response):
    return response.css('span._1F5u3 ::text').extract_first()

def get_date(response):
    return response.xpath('//div[@data-qa-id="adview_date"]//text()').extract_first()

def get_auteur(response):
    return response.css('div.T5Lvz ::text').extract_first()

def get_localisation(response):
    return response.css('div._1aCZv span::text').extract()

def get_buttons(response):
    return response.css('div._2sPVF ::text').extract()


def get_criteres(response):
    return response.css('div._277XW')


def get_next_list_of_announces(response):
    # Loading next page url
    next_page = response.css('a._1f-eo::attr(href)').extract()[-1]
    #logger.info('> NEXT PAGE : {}'.format(next_page))

    # Computing next_page number
    if 'page=' in next_page:
        next_page_number = int(next_page.split('page=')[1])
    elif 'p-' in next_page:
        next_page_number = int(next_page.split('p-')[1].replace('/', ''))
    else:
        next_page_number = None
    #logger.info('> NEXT PAGE NUMBER : {}'.format(next_page_number))
    return next_page, next_page_number