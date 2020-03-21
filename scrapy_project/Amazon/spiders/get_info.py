################################################################################################
################################################################################################
#                                       Main functions
################################################################################################
################################################################################################

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

################################################################################################
################################################################################################
#                                       Parsing main
################################################################################################
################################################################################################

def get_reference_links(response):
    return response.css('h2').xpath('a[contains(@class, "a-link-normal a-text-normal")]/@href').extract()


def get_main_pagination(response):
    next_page = response.css('ul.a-pagination > li.a-last ::attr(href)').extract_first()
    try:
        page_number = next_page.split('_')[-1]
        page_number = int(page_number)
    except:
        page_number = 100
    return next_page, page_number
    
################################################################################################
################################################################################################
#                                       Parsing a single referenec
################################################################################################
################################################################################################

def get_prices(response):
    price_1 = response.xpath('//h5//span[@class="a-color-price"]/text()').extract_first()
    price_2 = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first()
    price_3 = response.xpath('//span[@id="priceblock_saleprice"]/text()').extract_first()
    price_4 = response.xpath('//span[@id="newBuyBoxPrice"]/text()').extract_first()
    price_5 = response.xpath('//div[@id="olp_feature_div"]//span/text()').extract_first()
    return price_1, price_2, price_3, price_4, price_5

def get_title(response):
    title = response.xpath('//span[@id="productTitle"]/text()').extract_first()
    if title:
        title = title.replace('\n', '').replace('  ', '')
    return title

def get_description(response):
    description_1 = response.xpath('//div[contains(@id, "productDescription")]//p//text()').extract()
    description_2 = response.xpath('//div[contains(@class, "launchpad-text-left-justify")]//text()').extract()
    description = description_1 + description_2
    description = ','.join(description).replace('  ', '').replace('\n', '')
    return description

def get_items_description(response):
    texts = response.css('div#feature-bullets').xpath('ul/li/span/text()').extract()
    texts = [text.replace('\n', '').replace('\t', '') for text in texts]
    items_description = ','.join(texts).replace('  ', '')
    return items_description

def get_category(response):
    category = response.xpath('//ul[contains(@class, "a-unordered-list a-horizontal a-size-small")]//li//text()').extract()
    category = [cat.replace('\n', '').replace('  ', '') for cat in category]
    category = [cat for cat in category if len(cat) > 5]
    category = ', '.join(category)
    return category

