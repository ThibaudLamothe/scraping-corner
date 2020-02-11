import scrapy

class SpiderAmazon(scrapy.Spider):
    name = "AmazonSpider"

    def __init__(self, *args, **kwargs):
        super(SpiderAmazon, self).__init__(*args, **kwargs)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:
            self.start_urls =[
                # 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dindustrial-intl-ship&field-keywords='
                'https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A360832011&pf_rd_i=16225017011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=d51650ff-60b4-4a83-9258-120554589089&pf_rd_r=T0EBQZCJSG27SK4F0VHF&pf_rd_s=merchandised-search-4&pf_rd_t=101&ref=s9_acss_bw_cts_AELugg_T2_w'
            ]
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

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

        self.page = 0
        self.object = 0


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css('h2').xpath('a[contains(@class, "a-link-normal a-text-normal")]/@href').extract()
        print(links)
        for link in links:
            yield response.follow(url=link, callback=self.parse_object)

        next_page = response.css('ul.a-pagination > li.a-last ::attr(href)').extract_first()
        try:
            page_number = next_page.split('_')[-1]
            page_number = int(page_number)
        except:
            page_number = 100

        self.page += 1
        # if self.page < 3:
        if page_number <= 5:
            yield response.follow(next_page, callback=self.parse)

    def parse_object(self, response):
        self.object += 1
        print('*' * 60)
        print('*' * 60)
        print('Object number :', self.object)
        print('*' * 60)
        print('*' * 60)

        price = response.xpath('//h5//span[@class="a-color-price"]/text()').extract_first()
        price_2 = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first()
        price_3 = response.xpath('//span[@id="priceblock_saleprice"]/text()').extract_first()
        price_4 = response.xpath('//span[@id="newBuyBoxPrice"]/text()').extract_first()
        price_5 = response.xpath('//div[@id="olp_feature_div"]//span/text()').extract_first()

        title = response.xpath('//span[@id="productTitle"]/text()').extract_first()
        if title:
            title = title.replace('\n', '').replace('  ', '')


        description_1 = response.xpath('//div[contains(@id, "productDescription")]//p//text()').extract()
        description_2 = response.xpath('//div[contains(@class, "launchpad-text-left-justify")]//text()').extract()
        description = description_1 + description_2
        description = ','.join(description).replace('  ', '').replace('\n', '')

        texts = response.css('div#feature-bullets').xpath('ul/li/span/text()').extract()
        texts = [text.replace('\n', '').replace('\t', '') for text in texts]
        items_description = ','.join(texts).replace('  ', '')

        category = response.xpath('//ul[contains(@class, "a-unordered-list a-horizontal a-size-small")]//text()').extract()
        category = [cat.replace('\n', '').replace('  ', '') for cat in category]
        category = [cat for cat in category if len(cat) > 5]
        category = ', '.join(category)

        final_item = {
            'price_1':price,
            'price_2':price_2,
            'price_3':price_3,
            'price_4':price_4,
            'price_5':price_5,
            'category': category,
            'titre':title,
            'items':items_description,
            'description':description
        }
        for key, value in final_item.items():
            print('> ', key.upper(), '\n')
            print(value)
        yield final_item
