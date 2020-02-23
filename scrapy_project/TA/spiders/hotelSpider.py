# import scrapy
# from scrapy.spiders import CrawlSpider
# # from scrapy.TA import HotelreviewsItem


# class MySpider(CrawlSpider):
#     name = 'hotelTA'
#     domain_url = "https://www.tripadvisor.co.uk"
#     start_urls = [
#        'https://www.tripadvisor.co.uk/Restaurants-g191259-Greater_London_England.html',

#         # "https://www.tripadvisor.fr/Restaurant_Review-g60763-d6000258-Reviews-Up_Thai_restaurant-New_York_City_New_York.html"
#         ]

#     def parse(self, response):
#         print('HEEEEERE')

#         all_review_pages = response.xpath(
#             "//a[contains(@class,'pageNum') and contains(@class,'last')]/@data-offset").extract()

#         try:
#             next_reviews_page_url = "https://www.tripadvisor.com" + response.xpath(
#             "//a[contains(@class,'nav') and contains(@class,'next') and contains(@class,'primary')]/@href").extract()[0]
#         except:
#             next_reviews_page_url = None

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

#         item = HotelreviewsItem()

       
               
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

#         review_id = item["review_id"]
#         review_url_on_page = response.xpath('//script[@type="application/ld+json"]/text()').extract()
#         review = eval(review_url_on_page[0])

#         item["review"] = review["reviewBody"].replace("\\n", "")
#         item["title"] = review["name"]
#         item["rating"] = review["reviewRating"]["ratingValue"]
#         item["hotel_name"] = review["itemReviewed"]["name"]
#         try:
#             item["published_date"] = review["datePublished"]
#         except KeyError:

#             item["published_date"] = next(iter(response.xpath(
#                 f"//div[contains(@id,'review_{review_id}')]/div/div/span[@class='ratingDate']/@title""").extract()),
#                                           None)
#         try:
#             item["trip_date"] = next(iter(response.xpath("//div[contains(@class,"
#                                                          "'prw_reviews_resp_sur_h_featured_review')]/div/div/div/div["
#                                                          "contains(@class,'prw_reviews_stay_date_hsx')]/text()").extract(

#             )), None)

#         except:

#             item["trip_date"] = next(iter(response.xpath(
#                 "//div[contains(@id,'review_538163624')]/div/div/div[@data-prwidget-name='reviews_stay_date_hsx']/text()").extract()),
#                                      None)
#         yield item
