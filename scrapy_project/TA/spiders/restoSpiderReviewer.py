import scrapy

class QuotesSpider(scrapy.Spider):
    name = "restoTAreviewer"

    def __init__(self, *args, **kwargs): 
        super(QuotesSpider, self).__init__(*args, **kwargs) 
        
        # Parse URL
        self.start_urls = [kwargs.get('start_url')] 
        if self.start_urls == [None]:
            self.start_urls =[
                #'https://www.tripadvisor.fr/Restaurants-g60763-New_York_City_New_York.html#EATERY_OVERVIEW_BOX',
                'https://www.tripadvisor.co.uk/Restaurants-g191259-Greater_London_England.html' # zone
                # 'https://www.tripadvisor.co.uk/Restaurant_Review-g1480935-d13428223-Reviews-ITJL-Barnet_Greater_London_England.html' # resto
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def parse_resto(self, response):
        reviews = response.css('div.review-container')
        for review in reviews:
            title = review.css('span.noQuotes::text').extract_first()
            content = review.css('p.partial_entry::text').extract_first()
            rating_date = review.css('span.ratingDate::attr(title)').extract_first() 
            url = response.url
            # rating_value = 
            # name_rater
            # origin_rater
            # visit date


            comment_item = {
            'title':title,
            'content':content,
            'rating_date': rating_date,
            'url':url
            } 
            print('>>>', comment_item['title'])
            yield comment_item 
        
        xpath = '//a[@class="nav next taLnk ui_button primary"]'
        next_page = response.xpath(xpath)[0].css('::attr(href)').extract_first() 
        next_page_number = response.xpath(xpath)[0].css('::attr(data-page-number)').extract_first()


        #next_page = response.xpath('//*[@id="taplc_location_reviews_list_resp_rr_resp_0"]/div/div[14]/div/div/a[2]').css('::attr(href)').extract()[-1]
        #next_page_number = response.xpath('//*[@id="taplc_location_reviews_list_resp_rr_resp_0"]/div/div[14]/div/div/a[2]').css('::attr(data-page-number)').extract_first()

        if next_page is None:
            print(' - There is no next_page')
        else:
            print(' - There is a next_page')
            print(' - Page url is : {}'.format(next_page))
            if self.max_page is None:
                print(' - There is no number of page restriction. Go on.')
                yield response.follow(next_page, callback=self.parse_resto)
            else:
                print(' - Max page number is : {}'.format(self.max_page))

                if next_page_number is None:
                    print(' -  No next number page : STOP.')
                else:
                    print(' - Next page number is {}'.format(next_page_number))
                    if int(next_page_number) <= int(self.max_page):
                        print(' - It is smaller than limit. Go on.')
                        yield response.follow(next_page, callback=self.parse_resto)
                    else:
                        print('LIMIT was reached. STOP.')

    def parse(self, response):
      
        resto_items = response.css('div.restaurants-list-ListCell__infoWrapper--3agHz')
        for resto in resto_items:
            try:
                # Info annonce
                name = resto.css('a.restaurants-list-ListCell__restaurantName--2aSdo::text').extract_first()
                url = resto.css('a.restaurants-list-ListCell__restaurantName--2aSdo::attr(href)').extract_first()
                avis = resto.css('span.restaurants-list-ListCell__userReviewCount--2a61M::text').extract_first()
                nb_avis = avis[:-5].replace(' ', '')
                interm =  resto.css('span.restaurants-list-ListCell__infoRowElement--2E6E3::text').extract()
                descr_rapide = interm[1]
                prix_eur = interm[2]
                note_moyenne = resto.css('span.restaurants-list-ListCell__bubbleRating--1i1jl').extract_first().split('bubble_')[-1][0:2]
                note_moyenne = int(note_moyenne)
                

                #
                 
                print('\n', '*'*100,'\n', name,'\n', '*'*100)
                # print(url)
                # print('avis', avis)
                # print('nb_avis', nb_avis)
                # print('descr', descr_rapide)
                # print('prix : ',  prix_eur)
                # print('note', note_moyenne)

                final_item = {
                'name':name,
                'nb_avis':nb_avis,
                'note': note_moyenne,
                'prix': prix_eur,
                'descr':descr_rapide,
                'url':url
                } 
                #yield final_item  
                yield response.follow(url=url, callback=self.parse_resto)
            except:
                print('>>>> BUG !!!')



        xpath = '//a[@class="nav next rndBtn ui_button primary taLnk"]'
        next_page = response.xpath(xpath)[0].css('::attr(href)').extract_first() 
        next_page_number = response.xpath(xpath)[0].css('::attr(data-page-number)').extract_first()

        next_page = response.xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a').css('::attr(href)').extract()[-1]
        next_page_number = response.xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a').css('::attr(data-page-number)').extract_first()

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
