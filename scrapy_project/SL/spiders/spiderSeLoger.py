import scrapy

def isin_rep(rep, val='p'):

    p = [i for i in rep if val in i ]
    if len(p) ==1:
        p = p[0].split(' ')[0]
    else:
        p = None
    return p
                

class QuotesSpiderSL(scrapy.Spider):
    name = "spiderSL"

    def __init__(self, *args, **kwargs): 
        super(QuotesSpiderSL, self).__init__(*args, **kwargs)
        
        # Parse URL
        self.start_urls = [kwargs.get('start_url')] 
        if self.start_urls == [None]:
            self.start_urls =[
                'https://www.seloger.com/list.htm?enterprise=0&natures=1&places=[{ci:330522}|{ci:330318}|{ci:330281}|{ci:510454}|{ci:350238}|{ci:440109}|{ci:330063}|{ci:330039}]&price=50000/150000&projects=2&proximity=0,10&qsversion=1.0&types=1'
               #'https://www.seloger.com/list.htm?types=1&projects=2&enterprise=0&natures=1&price=90000%2F111000&places=%5B%7Bci%3A330522%7D%7C%7Bci%3A330318%7D%7C%7Bci%3A330039%7D%7C%7Bci%3A330281%7D%7C%7Bci%3A510454%7D%7C%7Bci%3A350238%7D%7C%7Bci%3A440109%7D%5D&qsVersion=1.0',
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
      
        sl_items = response.css('div.c-pa-list')
        print('COUOCU POPTO ZEROOOO')
        sl_items = response.xpath('//div[contains(@class,"block_ShadowedBlock")]/')
        print(len(sl_items))
        # Attention si l'on prend aussi les appartements neuf, on se rediriege vers un autre site
        # neuf.seloger.com => L'adresse url est différente et l'id aussi. On se retrouve avec des trucs bizarres en base
        # faire attention à bien filtrer uniquement sur les appartements ancie
        # NB : pas de garde fou dans le code.
        print('COUCOU POTO')
        for sl_item in sl_items:
            print('>>> SL ITEM')
            try:
                # Info annonce
                nb_pict = sl_item.css('span.media-count::text').extract_first()
                url = sl_item.css('a.c-pa-link::attr(href)').extract_first()
                id_ = url.split('.htm')[0].split('/')[-1]
                titre = sl_item.css('a.c-pa-link::attr(title)').extract_first()
                
                # Info bien
                prix_raw = sl_item.css('span.c-pa-cprice::text').extract_first()
                prix = str([tit for tit in prix_raw.split(' ') if len(tit)>2][0])
                ville = sl_item.css('div.c-pa-city::text').extract_first()
                
                # Info intérieur
                rep = sl_item.css('div.c-pa-criterion em::text').extract()
                # print('>> REP')
                # print(rep)
                


                nb_pieces = isin_rep(rep, 'p')
                nb_chambres = isin_rep(rep, 'ch')
                surface = isin_rep(rep, 'm²')
                etage = isin_rep(rep, 'etg')
                ascenceur = isin_rep(rep, 'asc')
                terasse = isin_rep(rep, 'tess')

                # Info agence
                code_postal = sl_item.css('em.agency-website::attr(data-codepostal)').extract_first()
                agence = sl_item.css('div::attr(alt)').extract_first()
                site_agence = sl_item.css('div a::attr(href)').extract()[-2]
                tel_agence = sl_item.css('a.tagClick.desktop.listContactPhone::attr(data-tooltip-focus)').extract_first()
                type_ = sl_item.css('div.c-pa-info a::text').extract_first()

                # Display in console
                print('\n', '*'*5, titre)
                print('Annonce N° : ', id_)
                print('Prix de vente', prix)
                print('Surface', surface)
                print(nb_pieces, 'pieces. Dont ', nb_chambres, 'chambres.')
                print('Située à ',  code_postal, ville)
                print('Vendu par', agence, site_agence, tel_agence)
                # print('Description complémentaire :', url)

                final_item = {
                'titre':titre,
                'id_':id_,
                'prix': prix,
                'surface': surface,
                'ville':ville,
                'code_postal':code_postal,
                'nb_pieces':nb_pieces,
                'nb_chambres':nb_chambres,
                'nb_pict':nb_pict,
                'etage':etage,
                'ascenceur':ascenceur,
                'terasse':terasse,
                'type':type_,
                'agence':agence,
                'tel_agence':tel_agence,
                'site_agence':site_agence,
                'url':url
            }

                yield final_item  
            except:
                print('>>>> BUG !!!')

        next_page = response.css('a.pagination-next::attr(href)').extract_first()
        next_page_number = None
        # if next_page is not None:
        #     # next_page = response.follow(next_page)
        #     print('>>> GOING TO NEXT PAGE !')
        #     yield response.follow(next_page, callback=self.parse)

        if next_page is None:
            print(' - There is no next_page')
        else:
            print(' - There is a next_page')
            print(' - Page url is : {}'.format(next_page))
            if self.max_page is None:
                print(' - There is no number of page restriction. Go on.')
                yield response.follow(next_page, callback=self.parse)
            else:
                print(' - Max page number is : {}'.format(self.max_page))
                if next_page_number is None:
                    print(' -  No next number page : STOP.')
                else:
                    print(' - Next page number is {}'.format(next_page_number))
                    if int(next_page_number) <= int(self.max_page):
                        print(' - It is smaller than limit. Go on.')
                        yield response.follow(next_page, callback=self.parse)
                    else:
                        print('LIMIT was reached. STOP.')

        # titre = response.css('span.c-pa-pprice::text').extract_first()
        # titre = [tit for tit in titre.split(' ') if len(tit)>2]
        # filename = 'SL_test.txt'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
