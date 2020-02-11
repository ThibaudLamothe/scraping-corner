# Scraping imports
import scrapy
from Amazon.spiders import get_info
from Amazon.items import AmazonItem

# Logging import
import logzero
import logging
from logzero import logger

class SpiderAmazon(scrapy.Spider):
    name = "AmazonSpider"

    def __init__(self, *args, **kwargs):
        super(SpiderAmazon, self).__init__(*args, **kwargs)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:

            # Luggage urls for Hackathon
            self.start_urls = [
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743251%2Cn%3A15743261&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=d51650ff-60b4-4a83-9258-120554589089&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-4&pf_rd_t=101&ref=s9_acss_bw_cts_AELugg_T1_w',
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A360832011&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=d51650ff-60b4-4a83-9258-120554589089&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-4&pf_rd_t=101&ref=s9_acss_bw_cts_AELugg_T2_w',
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743251%2Cn%3A15743271%2Cp_n_feature_eighteen_browse-bin%3A14630392011&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=d51650ff-60b4-4a83-9258-120554589089&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-4&pf_rd_t=101&ref=s9_acss_bw_cts_AELugg_T3_w',
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743241%2Cp_n_feature_eighteen_browse-bin%3A14630392011&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=d51650ff-60b4-4a83-9258-120554589089&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-4&pf_rd_t=101&ref=s9_acss_bw_cts_AELugg_T4_w',
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743251%2Cn%3A15743291&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=af558cb9-78a8-43e7-9cb3-a8cd207ee9af&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-5&pf_rd_t=101&ref=s9_acss_bw_cts_AELug3_T1_w',
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A9971584011&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=af558cb9-78a8-43e7-9cb3-a8cd207ee9af&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-5&pf_rd_t=101&ref=s9_acss_bw_cts_AELug3_T2_w',
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743251%2Cn%3A2477388011&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=af558cb9-78a8-43e7-9cb3-a8cd207ee9af&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-5&pf_rd_t=101&ref=s9_acss_bw_cts_AELug3_T3_w',
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743251%2Cn%3A2477386011&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=af558cb9-78a8-43e7-9cb3-a8cd207ee9af&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-5&pf_rd_t=101&ref=s9_acss_bw_cts_AELug3_T4_w',
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743231&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=fec43364-79a8-4f31-85ab-1ad18ec49011&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-6&pf_rd_t=101&ref=s9_acss_bw_cts_AELug2_T1_w',
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15744111&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=fec43364-79a8-4f31-85ab-1ad18ec49011&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-6&pf_rd_t=101&ref=s9_acss_bw_cts_AELug2_T2_w',
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743211&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=fec43364-79a8-4f31-85ab-1ad18ec49011&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-6&pf_rd_t=101&ref=s9_acss_bw_cts_AELug2_T3_w',
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743971&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=fec43364-79a8-4f31-85ab-1ad18ec49011&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-6&pf_rd_t=101&ref=s9_acss_bw_cts_AELug2_T4_w'
            ]

            # Categories url for Hackathon
            self.start_urls = [
                'https://www.amazon.com/s?i=electronics-intl-ship&rh=n%3A%2116225009011&page=2&qid=1581437527&ref=lp_16225009011_pg_2', # electronics
                'https://www.amazon.com/s?i=videogames-intl-ship&rh=n%3A%2116225016011&page=2&qid=1581437762&ref=lp_16225016011_pg_2', # videogames
                'https://www.amazon.com/s?i=pets-intl-ship&rh=n%3A%2116225013011&page=2&qid=1581438170&ref=lp_16225013011_pg_2', # pet supplies
                'http://amazon.com/s?i=sporting-intl-ship&rh=n%3A%2116225014011&page=2&qid=1581438225&ref=lp_16225014011_pg_2' # sports & outdoors
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


    def parse(self, response):

        # Number of main page scrapped
        self.page += 1

        # Get the url of each reference on the current page
        links = get_info.get_reference_links(response)

        # Follow these urls
        for link in links:
            yield response.follow(url=link, callback=self.parse_reference)

        # Get pagination information
        next_page, page_number = get_info.get_main_pagination(response)

        # Decision to follow a page or not
        if page_number <= 5:
            yield response.follow(next_page, callback=self.parse)


    def parse_reference(self, response):
        self.object += 1
        get_info.print_separation(self.object)

        # Get price informations
        price_1, price_2, price_3, price_4, price_5 = get_info.get_prices(response)

        # Get title information
        title = get_info.get_title(response)

        # Get description information
        description = get_info.get_description(response)

        # Get item description information
        items_description = get_info.get_items_description(response)

        # Get category information
        category = get_info.get_category(response)

        # Create item
        item = AmazonItem()
        item['price_1'] = price_1
        item['price_2'] = price_2
        item['price_3'] = price_3
        item['price_4'] = price_4
        item['price_5'] = price_5
        item['category'] = category
        item['titre'] = title
        item['items'] = items_description
        item['description'] = description

        # Display results
        for key, value in item.items():
            print('> ', key.upper(), '\n')
            print(value)

        # Store value as decided in the pipeline
        yield item
