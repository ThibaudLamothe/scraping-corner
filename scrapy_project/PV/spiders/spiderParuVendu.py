import scrapy
from PV.spiders import get_info
from ..items import PVItem

class SpiderPV(scrapy.Spider):
    name = "spiderPV"

    def __init__(self, *args, **kwargs):
        super(SpiderPV, self).__init__(*args, **kwargs)

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
        pv_items = get_info.get_items(response)

        # Attention si l'on prend aussi les appartements neuf, on se redirige vers un autre site
        # neuf.seloger.com => L'adresse url est différente et l'id aussi. On se retrouve avec des trucs bizarres en base
        # faire attention à bien filtrer uniquement sur les appartements ancien
        # NB : pas de garde fou dans le code.

        for pv_item in pv_items:
            try:

                # Get identificators
                url = get_info.get_url(pv_item)
                url = '{}{}'.format(website, url)
                id_ = url.split('/')[-1]
                print('*' * 25, 'START ITEM : ', id_, '*' * 25)

                # Get basic data
                titre = get_info.get_titre(pv_item)
                surface = titre.split('-')[-1].split(' ')[1]
                nb_pieces = int(titre.split('-')[-2].split(' ')[1])

                # Get localisation information
                ville_cp = get_info.get_ville_cp(pv_item)
                ville_cp = ville_cp.split('\n')[1]
                ville = ville_cp.split(' ')[0]
                code_postal = ville_cp.split(' ')[1][1:-2]

                # Compute final item
                item = PVItem()
                item['titre'] = titre
                item['id_'] = id_
                item['prix'] = get_info.get_prix(pv_item)
                item['surface'] = surface
                item['ville'] = ville
                item['code_postal'] = code_postal
                item['nb_pieces'] = nb_pieces
                item['nb_pict'] = get_info.get_nb_pict(pv_item)
                item['agence'] = get_info.get_agence(pv_item)
                item['url'] = url
                # item['small_decr']  = get_info.get_small_description(pv_item)
                yield item

            except:
                print('>> BUG : Peut etre un appartement neuf')

        print('> Dealing with next page.')
        next_page, next_page_number = get_info.get_next_list_of_annonces(response)
        if get_info.go_to_next_page(next_page, next_page_number, self.max_page):
            yield response.follow(next_page, callback=self.parse)