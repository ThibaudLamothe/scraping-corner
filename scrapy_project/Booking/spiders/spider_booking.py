import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
import sys
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from Booking.items import HotelreviewsItem
#from HotelReviews.helper_functions import user_info_splitter


class MySpider(CrawlSpider):
    name = 'BookingSpider'
    domain_url = "https://www.booking.com"
    # allowed_domains = ["https://www.tripadvisor.com"]

    # start_urls = ["https://www.tripadvisor.fr/Hotel_Review-g297549-d299638-Reviews-Mercure_Hurghada_Hotel-Hurghada"
    #              "_Red_Sea_and_Sinai.html"]
    start_urls = [
        "https://www.booking.com/reviewlist.fr.html?aid=397594;label=gog235jc-1DCAEoggI46AdIDVgDaE2IAQGYAQ24ARfIAQzYAQPoAQH4AQKIAgGoAgM;sid=68b0e620a0a3d91187ca55a989d415e2;cc1=fr;dist=1;pagename=les-bois-francs;srpvid=241646f376ce0a3e;type=total&;offset=0;rows=10;"]

    # rules = (
    # Extract links matching 'category.php' (but not matching 'subsection.php')
    # and follow links from them (since no callback means follow=True by default).
    # Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),

    # Extract links matching 'item.php' and parse them with the spider's method parse_item
    # Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
    # )

    def parse(self, response):

        try:
             next_reviews_page_url = "https://www.booking.com" + response.xpath("//a[contains(@class,'pagenext')]/@href").extract()[0]
             last_page = False
        except:
            last_page = True

        current_page_url = response.request.url
        print("##############################")
        print(current_page_url)
        print("#########")

        yield scrapy.Request(current_page_url, callback=self.parse_comment_page)

        if not last_page:
            yield scrapy.Request(next_reviews_page_url, callback=self.parse)

    def parse_comment_page(self, response):
        """

        :param response:
        :return:
        """
        item = HotelreviewsItem()
        item["review"] = response.request.url
        print("#####################################fffffffffffffffffff#########################################")
        yield item

        # all_reviews_blocks = response.xpath("//li[contains(@class,'new') and contains(@class,'block')]")
        # for block in all_reviews_blocks:
        #     item = HotelreviewsItem()
        #
        #     item["review"] = response.request.url
        #
        #     text = block.xpath(".//p/span/text()").extract()
        #     if len(text) == 2:
        #
        #         pass
        #
        #     else:
        #         print("##############################")
        #         review_sentiment = block.xpath(".//p/span/svg/@class").extract()[0]
        #         if "great" in review_sentiment:
        #             print("POSITIF")
        #             print(text)
        #         else:
        #             print("NEGATIF")
        #             print(text)
        #
        #     general_info = block.xpath(".//div/span/text()").extract()
        #     print(len(general_info))
        #
        #     yield item

            #print(block.xpath(".//p/span/text()").extract())
