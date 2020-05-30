################################################################################################
#                              DECIDING IF GOING TO NEXT PAGE OR NOT 
################################################################################################


def go_to_next_page(next_page, next_page_number, max_page, printing=False):
    if next_page is None:
        if printing: print(' - There is no next_page')
    else:
        if printing: print(' - There is a next_page')
        if printing: print(' - Page url is : {}'.format(next_page))
        if max_page is None:
            if printing: print(' - There is no number of page restriction. Go on.')
            # yield response.follow(next_page, callback=self.parse_resto)
            return True
        else:
            if printing: print(' - Max page number is : {}'.format(max_page))

            if next_page_number is None:
                if printing: print(' -  No next number page : STOP.')
            else:
                if printing: print(' - Next page number is {}'.format(next_page_number))
                if int(next_page_number) <= int(max_page):
                    if printing: print(' - It is smaller than limit. Go on.')
                    # yield response.follow(next_page, callback=self.parse_resto)
                    return True
                else:
                    if printing: print('LIMIT was reached. STOP.')
    return False


################################################################################################
################################################################################################
#                                        NAVIGATION 
################################################################################################
################################################################################################

def get_urls_cocktails_in_main_search_page(response):    
    css = 'section >  article a ::attr(href)'
    urls = response.css(css).extract()
    urls = [url for url in urls if '/recipe/' in url]
    return urls


def get_urls_next_list_of_cocktails(response):
    xpath_1 = '//*[@class="recipe-paging clearfix"]'
    xpath_2 = '//*[@class="last asset-font"]'

    next_page_link = response.xpath(xpath_1).xpath(xpath_2)
    next_page = next_page_link.css('::attr(href)').extract_first()
    next_page_number = next_page_link.css('::attr(data-page)').extract_first()
    return next_page, next_page_number



################################################################################################
################################################################################################
#                                       COCKTAIL INFORMATION 
################################################################################################
################################################################################################

def get_url(response):
    return response.url

def get_cocktail_name(response):
    return response.css('h1.item-title ::text').extract_first()

def get_cocktail_picture_url(response):
    return response.css('div.item-hero-img img ::attr(src)').extract_first()  

def get_cocktail_level(response):
    return response.css('div.item-difficulty span ::text').extract_first()  

def get_cocktail_rating(response):
    return response.css('span.item-rating-count ::text').extract_first()

def get_cocktail_nb_reviews(response):
    return response.css('span.item-rating-count ::text').extract_first()

def get_cocktail_description(response):
    return response.css('div.item-summary p ::text').extract_first() 

def get_ingredients_panel(response):
    return response.css('div.ingredients ul.instruction-item-list li' )

def get_cocktail_ingredient_dict(ingredients):
    ingredient_dict = {}
    for ingredient in ingredients[:-1]: # the last is the quantity of alochol
        quantite = ingredient.css('i> span ::text').extract()[0] 
        unite = ingredient.css('i> span ::text').extract()[1] 
        name = ingredient.css('div ::text').extract_first().strip()
        ingredient_dict[name] = {'quantite':quantite, 'unite':unite}
    return ingredient_dict

def get_cocktail_alcool_quantity(ingredients):
    return ingredients[-1].css('i.instruction-item-list-detail ::text').extract_first().strip()

def get_cocktail_equipment_dict(response):
    equipment_dict = {}
    css = 'div.equipment ul.instruction-item-list li' 
    equipments = response.css(css)
    for equipment in equipments:
        name = equipment.css('div ::text').extract()
        quantite = equipment.css('i > span ::text').extract_first()
        
        # Alternative to detect earlier if there is a link on the name
        if len(name)==3:  # when itt was a link, text around it
            name = name[1].strip()
        elif len(name)==1: # when no link there is only one text
            name = name[0].strip()
        else:
            logger.error('No name for that equipment.')
        equipment_dict[name] = quantite
    return equipment_dict

def get_cocktail_instructions_list(response):
    css = 'ol.method-list li'
    instructions = response.css(css)
    instructions_list = []
    for nb, instruction in enumerate(instructions):
        primary = ' '.join(instruction.css('div ::text').extract())
        secondary = ' '.join(instruction.css('p ::text').extract())
        instructions_list.append([primary, secondary])
    return instructions_list


def get_cocktail_tags(response):
    return response.css('ul.item-tags-list li ::text').extract()
