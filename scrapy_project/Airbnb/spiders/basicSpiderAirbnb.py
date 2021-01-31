import scrapy
from logzero import logger as lg
class SpiderAirbnb(scrapy.Spider):
    name = "BasicAirbnbSpider"

    def start_requests(self):
        cities = ['toronto']
        urls = [f'https://www.airbnb.com/s/{city}/homes/' for city in cities]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
           

    def parse(self, response):
        lg.info(response.url)

        # Gettting the hotels list
        hotels = response.css('div._8ssblpx')

        # Iterating over each of them
        for hotel in hotels:

            # Get main information
            title            = hotel.css('a ::attr(aria-label)').extract_first()
            url_link         = hotel.css('::attr(href)').extract_first()
            url_img          = hotel.css('img ::attr(src)').extract_first()
            type_of_room     = hotel.css('div._b14dlit ::text').extract_first()

            # Get tag information
            additionnal_info = hotel.css('div._kqh46o ::text').extract()
            additionnal_info = [i for i in additionnal_info if i not in [' · ']]

            # Get rating information
            rating = hotel.css('span._10fy1f8 ::text').extract()
            if rating != []:
                rating = rating[0]

            nb_comment = hotel.css('span._a7a5sx ::text').extract()
            if nb_comment != []:
                nb_comment = nb_comment[1]

            # Is it a airbnb "superhost" ?
            superhost        = hotel.css('div._ufoy4t::text').extract()
            superhost        = 'SUPERHOST' in superhost
            lg.debug(title)
            yield {
                'titre'            : title,
                'url_scrapped'     : response.url,
                'url_link'         : url_link,
                'url_img'          : url_img,
                'type_of_room'     : type_of_room,
                'additionnal_info' : additionnal_info,
                'rating'           : rating,
                'nb_comment'       : nb_comment,
                'superhost'        : superhost
                }
        
        # Get Next Page information
        next_page = response.css('a._za9j7e ::attr(href)').extract()
        lg.info(next_page)
        if next_page is not None:
            if len(next_page)>0:
                next_page = next_page[0]
                url = "https://www.airbnb.com" + next_page + '&display_currency=USD'
                lg.info(url)
                yield scrapy.Request(url=url, callback=self.parse)     
       