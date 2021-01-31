# Scraping imports
import scrapy
# from Airbnb.items import AirItem
# from Airbnb.spiders import get_info
# from scrapy_splash import SplashRequest

# Logging import
import logzero
import logging
from logzero import logger as lg

logzero.loglevel(logging.DEBUG) # To display content information
# logzero.loglevel(logging.INFO)  # To see number of parsed references
#logzero.loglevel(logging.WARN)  # To see number of parsed main pages

class SpiderAirbnb(scrapy.Spider):
    name = "AirbnbSpider"

    def __init__(self, *args, **kwargs):
        super(SpiderAirbnb, self).__init__(*args, **kwargs)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:

            # Categories url for Hackathon
            self.start_urls = [
                # 'https://www.airbnb.com/s/Manhattan--New-York--NY--United-States/homes?source=structured_search_input_header&search_type=unknown&tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=calendar&ne_lat=41.01482653192494&ne_lng=-73.7149411480591&sw_lat=40.31377538732325&sw_lng=-74.1983395855591&zoom=10&search_by_map=true'
                "https://www.airbnb.com/s/manhattan/homes/" + '?checkin=2021-02-10&checkout=2021-02-12&display_currency=USD'  + '&price_min=0&price_max=100',
                "https://www.airbnb.com/s/manhattan/homes/" + '?checkin=2021-02-10&checkout=2021-02-12&display_currency=USD'  + '&price_min=100&price_max=120',
                "https://www.airbnb.com/s/manhattan/homes/" + '?checkin=2021-02-10&checkout=2021-02-12&display_currency=USD'  + '&price_min=120&price_max=140',
                "https://www.airbnb.com/s/manhattan/homes/" + '?checkin=2021-02-10&checkout=2021-02-12&display_currency=USD'  + '&price_min=140&price_max=160'
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

        # Scrapping compteur
        self.page = 0
        self.object = 0


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # yield SplashRequest(url=url, callback=self.parse, args={'wait':2})


    def parse(self, response):

        # Number of main page scrapped
        self.page += 1
        lg.warn('Parse page ({})'.format(self.page))

        # Get the url of each reference on the current page
        # links = get_info.get_reference_links(response)

        # annonces = response.css('a._gjfol0')
        annonces = response.css('div._8ssblpx')
        for annonce in annonces:
            titre = annonce.css('a ::attr(aria-label)').extract_first()
            lien = annonce.css('::attr(href)').extract_first()
            img_url = annonce.css('img ::attr(src)').extract_first()
            type_of_room = annonce.css('div._b14dlit ::text').extract_first()

            additionnal_info = annonce.css('div._kqh46o ::text').extract()
            additionnal_info = [i for i in additionnal_info if i not in [' · ']]

            rating = annonce.css('span._10fy1f8 ::text').extract_first()
            nb_comment = annonce.css('span._a7a5sx ::text').extract()
            # nb_comment = nb_comment[1]

            night_price = annonce.css('span._1p7iugi ::text').extract()
            full_price = annonce.css('span._7nl8mr ::text').extract()

            superhost = annonce.css('div._ufoy4t::text').extract()
            superhost = 'SUPERHOST' in superhost
            lg.debug(titre)
            yield {
                'titre':titre,
                'lien':lien,
                'img_url':img_url,
                'type_of_room':type_of_room,
                'additionnal_info':additionnal_info,
                'rating':rating,
                'nb_comment':nb_comment,
                'night_price':night_price,
                'full_price':full_price,
                'superhost':superhost

                }
        # Follow these urls
        # for link in links:
            # yield response.follow(url=link, callback=self.parse_reference)
            # link = 'https://www.amazon.com' + link
            # yield SplashRequest(url=link, callback=self.parse_reference, args={'wait':5})

        # next_page = response.xpath('//a[contains(@aria-label, "Next")]').css('::attr(href)').extract_first()
        #next_page = response.xpath('//div[contains(@aria-label, "pagination")]//a[contains(@aria-label, "Next")]').css('::attr(href)').extract_first()
        next_page = response.css('a._za9j7e ::attr(href)').extract()
        lg.error(next_page)
        lg.error(len(next_page))
        if next_page is not None:
            if len(next_page)>0:
                next_page = next_page[0]
                lg.error(next_page)
                lg.info(self.page)
                # if self.page < 15:
                lg.info('Going to next')
                # yield response.follow(next_page, callback=self.parse)
                url = "https://www.airbnb.com" + next_page + '&display_currency=USD'
                lg.info(url)
                yield scrapy.Request(url=url, callback=self.parse)
        else:
            lg.error('No next page')
        # Get pagination information
        # next_page, page_number = get_info.get_main_pagination(response)

        # Decision to follow a page or not
        # if page_number <= 120:
            
            # yield response.follow(next_page, callback=self.parse)
            # next_page = 'https://www.amazon.com' + next_page
            # yield SplashRequest(url=next_page, callback=self.parse, args={'wait':10})



    # def parse_reference(self, response):
    #     self.object += 1
    #     logger.info('Parse object ({})'.format(self.object))
    #     logger.debug(response.url)

    #     # Get price informations
    #     prices = get_info.get_prices(response)
    #     price_1, price_2, price_3, price_4, price_5 = prices
    #     logger.debug(prices)

    #     # Get title information
    #     title = get_info.get_title(response)
    #     logger.debug(title)

    #     # Get description information
    #     description = get_info.get_description(response)

    #     # Get item description information
    #     items_description = get_info.get_items_description(response)

    #     # Get category information
    #     category = get_info.get_category(response)

    #     # Create item
    #     item = AmazonItem()
    #     item['price_1'] = price_1
    #     item['price_2'] = price_2
    #     item['price_3'] = price_3
    #     item['price_4'] = price_4
    #     item['price_5'] = price_5
    #     item['category'] = category
    #     item['choice_scrap'] = 'sports'
    #     item['titre'] = title
    #     item['items'] = items_description
    #     item['description'] = description
    #     item['url'] = response.url

    #     # Store value as decided in the pipeline
    #     yield item
