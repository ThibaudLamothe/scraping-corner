
import scrapy
import json
import time
import platform
import datetime

from ..items import AnnonceItem

def is_url_already_in_db(url_id, id_list):
    print('> Checking if ID : {} already in db'.format(url_id))
    # print(id_list)
    id_list = [str(i) for i in id_list]
    print('  {}'.format(str(url_id) in id_list))
    return str(url_id) in id_list

def print_star(text, nb_star=25):
    print('\n', '#'*nb_star, text, '#'*nb_star, '\n')



def critere_cleaning(criteres):
    dict_crit = {}
    for crit in criteres.xpath('div'):
        extraction_crit = crit.css('::text').extract()
        critere_name = extraction_crit[0]
        critere_value = extraction_crit[1]
        print('CRITERE : ', critere_name)
        if (critere_name == 'GES') or (critere_name=='Classe énergie'):#('Classe' in critere_name and 'nergie' in critere_name) :
            print('Specific criter')
            critere_value = 'NA'
        dict_crit[critere_name] = critere_value
    return dict_crit


class QuotesSpider(scrapy.Spider):
    name = "spiderLBC"


    def __init__(self, *args, **kwargs): 
        super(QuotesSpider, self).__init__(*args, **kwargs) 
        
        # Parse URL
        self.start_urls = [kwargs.get('start_url')] 
        if self.start_urls == [None]:
            self.start_urls =[
                'https://www.leboncoin.fr/recherche/?category=9&locations=Nantes,Rennes,Reims_51100,Bordeaux,Talence_33400,Pessac_33600,M%C3%A9rignac_33700&real_estate_type=2&immo_sell_type=old&price=75000-125000'
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_main)


    def parse_annonce(self, response):
         
        id_ = response.url.split('/')[-2].split('.')[0]
        print_star('Parsing annonce : {}'.format(id_), 15)
        
        item = AnnonceItem()
        
        print('- Get basic data on Annonce page')
        # titre =  response.css('h1._1KQme ::text').extract_first()
        titre =  response.css('h1._246DF ::text').extract_first()
        description = response.css('span.content-CxPmi ::text').extract()
        prix = response.css('span._1F5u3 ::text').extract_first()
        date_absolue = response.xpath('//div[@data-qa-id="adview_date"]//text()').extract_first()
        auteur =  response.css('div.T5Lvz ::text').extract_first()
        localisation = response.css('div._1aCZv span::text').extract()
        ville = localisation[0]
        code_postal = localisation[-1]
        buttons = response.css('div._2sPVF ::text').extract()
        
        print('- Check buttons')
        is_numero = False
        if 'Voir le numéro' in buttons:
            is_numero = True
        is_envoi_msg = False
        if 'Envoyer un message' in buttons:
            is_envoi_msg = True

        print('- Get Criteres')
        criteres = response.css('div._277XW')
        criteres_dict = critere_cleaning(criteres)
        print(criteres_dict)

        print('- Get other data from main page')
        # nb_pict = self.results[id_]['nb_pict']
        # categorie = self.results[id_]['categorie']
        nb_pict = 3 #self.results[id_]['nb_pict']
        categorie = 'cat' # self.results[id_]['categorie']

        item['id_'] = id_
        item['url'] = response.url
        item['titre'] = titre
        item['description'] = description
        item['prix'] = prix
        item['date_absolue'] = date_absolue
        item['auteur'] = auteur
        item['ville'] = ville
        item['code_postal'] = code_postal
        item['is_msg'] = is_envoi_msg
        item['is_num'] = is_numero
        item['critere'] = criteres_dict
        item['nb_pict'] = nb_pict
        item['categorie'] = categorie   
        
        yield item


    def parse_main(self, response):
        
        print('> Getting items list')
        lbc_items = response.css('li._3DFQ-')
        print('> Found {} items.'.format(len(lbc_items)))
        now = str(datetime.datetime.now())
        
        for lbc_item in lbc_items:
            print_star('Dealing with new item', 25)
            lbc_item = lbc_item.xpath('.')
            titre = lbc_item.css('p._2tubl span::text').extract_first()
            print('> Parsing : {} on main page'.format(titre))

            url = lbc_item.css('a::attr(href)').extract_first()
            url_id = url.split('/')[-2].split('.')[0]
            prix = lbc_item.css('span._1NfL7::text').extract_first()
            categorie = lbc_item.css('p.CZbT3::text').extract_first()
            lieu = lbc_item.css('p._2qeuk::text').extract_first()
            date = lbc_item.css('p.mAnae::text').extract_first()
            nb_pict = lbc_item.css('span._2lY3w span:nth-of-type(2)::text').extract_first()            

            information_main_page = {'titre':titre, 'url':url, 'prix':prix, 'categorie':categorie, 'lieu':lieu, 'date':date, 'nb_pict':nb_pict}
            print('> Results found : ', list(information_main_page.keys()))
            
            yield response.follow(url=url, callback=self.parse_annonce)
            
            #yield information_main_page    


        # Following next page        
        print_star('ANALYSE OF NEXT PAGES', 30)
        
        # Loading next page url
        next_page =  response.css('a._1f-eo::attr(href)').extract()[-1]
        print('> NEXT PAGE : {}'.format(next_page))
        
        # Computing next_page number
        if 'page=' in next_page:
            next_page_number = int(next_page.split('page=')[1])
        elif 'p-' in next_page:
            next_page_number = int(next_page.split('p-')[1].replace('/',''))
        else:
            next_page_number = None
        print('> NEXT PAGE NUMBER : {}'.format(page_seen))

        # if next_page is not None and page_seen < nb_max_page:
        #     # yield scrapy.Request(next_page, callback=self.parse_main)
        #     yield response.follow(next_page, callback=self.parse_main)
        

        if next_page is None:
            print(' - There is no next_page')
        else:
            print(' - There is a next_page')
            print(' - Page url is : {}'.format(next_page))
            if self.max_page is None:
                print(' - There is no number of page restriction. Go on.')
                yield response.follow(next_page, callback=self.parse_main)
            else:
                print(' - Max page number is : {}'.format(self.max_page))
                if next_page_number is None:
                    print(' -  No next number page : STOP.')
                else:
                    print(' - Next page number is {}'.format(next_page_number))
                    if int(next_page_number) <= int(self.max_page):
                        print(' - It is smaller than limit. Go on.')
                        yield response.follow(next_page, callback=self.parse_main)
                    else:
                        print('LIMIT was reached. STOP.')
