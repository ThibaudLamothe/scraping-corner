# import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from HotelReviews.items import HotelReviewsItem


# # TODO: Gerer price range, adresse, voir pour reponse manager, changer le join d'url
# # TODO: Ajout des notes par catégories
# # TODO: Régler problème encoding


# class MySpider(CrawlSpider):
#     name = 'BasicSpider'
#     domain_url = "https://www.tripadvisor.com"
#     # scraallowed_domains = ["https://www.tripadvisor.com"]

#     # start_urls = ["https://www.tripadvisor.fr/Hotel_Review-g297549-d299638-Reviews-Mercure_Hurghada_Hotel-Hurghada"
#     #              "_Red_Sea_and_Sinai.html"]
#     start_urls = [
#         "https://www.tripadvisor.fr/Restaurant_Review-g60763-d6000258-Reviews-Up_Thai_restaurant-New_York_City_New_York.html"
#         # "https://www.tripadvisor.fr/Hotel_Review-g209964-d523986-Reviews-Center_Parcs_Longleat_Forest-Warminster_Wiltshire_England.html",
#         # "https://www.tripadvisor.fr/Hotel_Review-g678202-d1100598-Reviews-Center_Parcs_Les_Bois_Francs-Verneuil_sur_Avre_Verneuil_d_Avre_et_d_Iton_Eure_Haute_No.html",
#         # "https://www.tripadvisor.fr/Hotel_Review-g1079438-d1486314-Reviews-Center_Parcs_les_Hauts_de_Bruyeres-Chaumont_sur_Tharonne_Loir_et_Cher_Centre_Val_de_L.html",
#         # "https://www.tripadvisor.fr/Hotel_Review-g1573379-d1573383-Reviews-Center_Parcs_Les_Trois_Forets-Hattigny_Moselle_Grand_Est.html",
#         # "https://www.tripadvisor.fr/Hotel_Review-g1572451-d775381-Reviews-Center_Parcs_Le_Lac_d_Ailette-Chamouille_Aisne_Hauts_de_France.html",
#         # "https://www.tripadvisor.fr/Hotel_Review-g5555792-d7107948-Reviews-Center_Parcs_Le_Bois_aux_Daims-Les_Trois_Moutiers_Vienne_Nouvelle_Aquitaine.html"

#     # "https://www.tripadvisor.fr/Hotel_Review-g2470936-d573930-Reviews-Center_Parcs_Elveden_Forest-Elveden_Suffolk_East_Anglia_England.html",
#     # "https://www.tripadvisor.fr/Hotel_Review-g1955842-d300038-Reviews-Center_Parcs_Sherwood_Forest-Rufford_Nottinghamshire_England.html",
#     # "https://www.tripadvisor.fr/Hotel_Review-g190737-d6117690-Reviews-Center_Parcs_Woburn_Forest-Bedford_Bedfordshire_England.html",
#     # "https://www.tripadvisor.fr/Hotel_Review-g186328-d1209793-Reviews-Center_Parcs_Whinfell_Forest-Penrith_Eden_District_Lake_District_Cumbria_England.html"
#     ]

#     # rules = (
#     # Extract links matching 'category.php' (but not matching 'subsection.php')
#     # and follow links from them (since no callback means follow=True by default).
#     # Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),

#     # Extract links matching 'item.php' and parse them with the spider's method parse_item
#     # Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
#     # )

#     def parse(self, response):

#         all_review_pages = response.xpath(
#             "//a[contains(@class,'pageNum') and contains(@class,'last')]/@data-offset").extract()

#         try:
#             next_reviews_page_url = "https://www.tripadvisor.com" + response.xpath(
#             "//a[contains(@class,'nav') and contains(@class,'next') and contains(@class,'primary')]/@href").extract()[0]
#         except:
#             next_reviews_page_url = None

#         # next_page_number = eval(response.xpath(
#         #      "//a[contains(@class,'nav') and contains(@class,'next') and contains(@class,'primary')]/@data-page-number").extract()[
#         #                              0])

#         #if next_page_number < 10:
#         try:
#             yield scrapy.Request(next_reviews_page_url, callback=self.parse)
#         except:
#             pass

#         review_urls = []

#         full_reviews_url = response.xpath("//div[contains(@class,'quote')]/a/@href").extract()
#         if not full_reviews_url:
#             full_reviews_url = response.xpath("//div[@dir='ltr']/a/@href").extract()

#         for partial_review_url in full_reviews_url:
#             review_url = response.urljoin(partial_review_url)
#             if review_url not in review_urls:
#                 review_urls.append(review_url)
#             yield scrapy.Request(review_url, callback=self.parse_review_page)

#     def parse_review_page(self, response):

#         item = HotelReviewsItem()

#         item["reviewer_id"] = next(iter(response.xpath(
#             "//div[contains(@class,'prw_reviews_resp_sur_h_featured_review')]/div/div/div/div/div[contains(@class,'prw_reviews_user_links_hs')]/span/@data-memberid").extract()),
#                                    None)
#         item["review_language"] = next(iter(response.xpath(
#             "//div[contains(@class,'prw_reviews_resp_sur_h_featured_review')]/div/div/div/div/div[contains(@class,'prw_reviews_user_links_hs')]/span/@data-language").extract()),
#                                        None)
#         item["review_id"] = next(iter(response.xpath(
#             "//div[contains(@class,'prw_reviews_resp_sur_h_featured_review')]/div/div/div/div/div[contains(@class,'prw_reviews_user_links_hs')]/span/@data-reviewid").extract()),
#                                  None)
#         item["review_id"] = next(iter(response.xpath(
#             "//div[contains(@class,'prw_reviews_resp_sur_h_featured_review')]/div/div/div/div/div[contains(@class,'prw_reviews_user_links_hs')]/span/@data-reviewid").extract()),
#                                  None)

#         # item["pid"] = next(iter(response.xpath(
#         #     "//div[contains(@class,'prw_reviews_resp_sur_h_featured_review')]/div/div/div/div/div[contains(@class,'prw_reviews_user_links_hs')]/span/@data-pid").extract()),
#         #                    None)
#         # item["locid"] = next(iter(response.xpath(
#         #     "//div[contains(@class,'prw_reviews_resp_sur_h_featured_review')]/div/div/div/div/div[contains(@class,'prw_reviews_user_links_hs')]/span/@data-locid").extract()),
#         #                      None)

#         review_id = item["review_id"]
#         review_url_on_page = response.xpath('//script[@type="application/ld+json"]/text()').extract()
#         review = eval(review_url_on_page[0])

#         item["review"] = review["reviewBody"].replace("\\n", "")
#         item["title"] = review["name"]
#         item["rating"] = review["reviewRating"]["ratingValue"]
#         # item["image_url"] = review["image"]
#         # item["hotel_type"] = review["itemReviewed"]["@type"]
#         item["hotel_name"] = review["itemReviewed"]["name"]
#         # item["price_range"] = review["itemReviewed"]["priceRange"]
#         # item["hotel_adress"] = review["itemReviewed"]["address"]
#         try:
#             item["published_date"] = review["datePublished"]
#         except KeyError:

#             item["published_date"] = next(iter(response.xpath(
#                 f"//div[contains(@id,'review_{review_id}')]/div/div/span[@class='ratingDate']/@title""").extract()),
#                                           None)

#         # item["trip_type"] = next(iter(response.xpath("//div[contains(@class,"
#         #                                              "'prw_reviews_resp_sur_h_featured_review')]/div/div/div/div/div"
#         #                                              "/div/div/div[contains(@class,'noRatings')]/text()").extract()),
#         #                          None)

#         try:
#             item["trip_date"] = next(iter(response.xpath("//div[contains(@class,"
#                                                          "'prw_reviews_resp_sur_h_featured_review')]/div/div/div/div["
#                                                          "contains(@class,'prw_reviews_stay_date_hsx')]/text()").extract(

#             )), None)

#         except:

#             item["trip_date"] = next(iter(response.xpath(
#                 "//div[contains(@id,'review_538163624')]/div/div/div[@data-prwidget-name='reviews_stay_date_hsx']/text()").extract()),
#                                      None)

#         # user_info = response.xpath("//div[contains(@class,'prw_reviews_resp_sur_h_featured_review')]/div/div/div/div/div[contains(@class,'prw_reviews_user_links_hs')]").extract()[0]
#         # item["unstructured"] = user_info_splitter(user_info)

#         yield item
