from logzero import logger

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


# filename = 'test_html_{}.html'.format(self.page)
# with open(filename, 'wb') as f:
#     f.write(response.body)
# # self.log('Saved file %s' % filename)


################################################################################################
################################################################################################
#                                       Parsing main
################################################################################################
################################################################################################

def get_links(response):

    css_selector = 'ul.product-grid > li.product-grid-item article div div a ::attr(href)'
    # logger.debug(css_selector)

    links = response.css(css_selector).extract()
    # logger.debug(len(links))

    links = set(links)
    # logger.debug(links)

    links = [link for link in links if '/p/' in link]


    return links


################################################################################################
################################################################################################
#                                       Parsing article
################################################################################################
################################################################################################

def get_description(response):
    return response.css('p.paragraph ::text').extract()


def get_description2(response):
    return response.xpath("//div[@class='pdp__secondary']//ul[@type='disc']//span//text()").extract()


def get_titre(response):
    selector = 'div.main-details__wrap > div> h1 ::text'
    return response.css(selector).extract()


def get_soustitre(response):
    selector = 'div.main-details__wrap > div> span ::text'
    return response.css(selector).extract()


def get_price(response):
    selector = 'div.pdp__product'
    selector2 = 'div.pdp-pricing__group > div:nth-of-type(1) ::text'
    return response.css(selector).css(selector2).extract()


def get_similaire(response):
    selector = '//h2[contains(@class, "ds-title ds-title--medium")]//text()'
    soustitre = response.xpath(selector).extract()
    return soustitre


def get_picture_url(response):
    try:


        selector = 'div.pdp__product div.pdp-hero__images div ::attr(style)'
        logger.debug(selector)

        pictures = response.css(selector).extract()  # .css(selector2).extract()
        picture = [i for i in pictures if '.jpg' in i][0]
        logger.debug(picture)

        picture = picture.replace('url(', ' ').replace('?placeholder', ' ')
        logger.debug(picture)

        picture = picture.split()
        logger.debug(picture)

        picture_url = [i for i in picture if '.jpg' in i][0]
        logger.debug(picture_url)

        # picture_url = 'www.carrefour.fr' + picture
        picture_url_small = picture_url.replace('1500x1500', '540x540')
    except:
        picture_url = None
    return [picture_url]


def get_position(response):
    selector = 'nav.pdp__nav ol.breadcrumb-trail__list li a ::text'
    return response.css(selector).extract()