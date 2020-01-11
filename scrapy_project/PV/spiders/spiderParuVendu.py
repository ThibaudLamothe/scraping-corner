import scrapy

def isin_rep(rep, val='p'):

    p = [i for i in rep if val in i ]
    if len(p) ==1:
        p = p[0].split(' ')[0]
    else:
        p = None
    return p


class QuotesSpider(scrapy.Spider):
    name = "spiderPV"

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:
            self.start_urls =[
                'https://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?nbp=0&tt=1&tbApp=1&tbDup=1&tbChb=1&tbLof=1&at=1&nbp0=99&px0=90000&px1=111000&pa=FR&ddlFiltres=nofilter&codeINSEE=44XX0,35XX0,51454,33281,33318,33522,'
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        website = 'https://www.paruvendu.fr'
        pv_items = response.css('div.ergov3-annonce')

        # Attention si l'on prend aussi les appartements neuf, on se rediriege vers un autre site
        # neuf.seloger.com => L'adresse url est différente et l'id aussi. On se retrouve avec des trucs bizarres en base
        # faire attention à bien filtrer uniquement sur les appartements ancie
        # NB : pas de garde fou dans le code.

        for pv_item in pv_items:
            try:
                print('*' * 50)
                print('> START ITEM')
                prix = pv_item.css('div.ergov3-priceannonce::text').extract()[1].split('\n')[1].split('€')[0]
                titre = pv_item.css('div.ergov3-annonce a:nth-child(2)::attr(title)').extract_first()
                # titre = pv_item.css('a.voirann::attr(title)').extract_first()
                surface = titre.split('-')[-1].split(' ')[1]
                nb_pieces = int(titre.split('-')[-2].split(' ')[1])
                ville_cp = pv_item.css('div.ergov3-txtannonce cite').extract_first()
                ville_cp = ville_cp.split('\n')[1]
                ville = ville_cp.split(' ')[0]
                code_postal = ville_cp.split(' ')[1][1:-2]
                nb_pict = pv_item.css('span.re14_nbphotos::text').extract_first()
                agence = pv_item.css('div.ergov3-bottomannonce div img::attr(alt)').extract_first()
                small_description = pv_item.css('div.ergov3-txtannonce p::text').extract()
                url = pv_item.css('a.voirann::attr(href)').extract_first()
                url = '{}{}'.format(website, url)
                id_ = url.split('/')[-1]
                print('> Compute final item')

                final_item = {
                    'titre': titre,
                    'annonce': id_,
                    'prix': prix,
                    'surface': surface,
                    'ville': ville,
                    'code_postal': code_postal,
                    'nb_pieces': nb_pieces,
                    'nb_pict': nb_pict,
                    'agence': agence,
                    'url': url
                }

                # print(final_item)
                print('> END ITEM')

                yield final_item
            except:
                print('>>>> BUG !!!')
                print('Peut etre un appartement neuf')

        print('> Dealing with next page.')
        next_page = response.css('div.pv15-pagsuiv ::attr(href)').extract()[-1]
        next_page_number = int(next_page.split('&p=')[-1]) if len(next_page.split('&p=')) > 0 else None

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
