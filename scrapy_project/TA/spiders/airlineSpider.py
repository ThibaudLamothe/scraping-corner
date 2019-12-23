from scrapy.TA import TripAdvisorAirlineItem
from scrapy import Spider, Request
import re

class TripAdvisor(Spider):
    name='airlineTA'
    allowed_urls=['https://www.tripadvisor.ca']
    start_urls=['https://www.tripadvisor.co.uk/Airline_Review-d8729141-Reviews-Ryanair',
                'https://www.tripadvisor.co.uk/Airline_Review-d8729066-Reviews-EasyJet',
                'https://www.tripadvisor.co.uk/Airline_Review-d8729171-Reviews-Transavia'
                ]

    def verify(self, page_list):
        if isinstance(page_list, list):
            if len(page_list) == 1:
                return page_list[0]
                # In Python 2, everything you scraped is in unicode, which might cause some trouble when you save it to local file.
                # The rule of thumb is to encode it with ascii using the following command.
                # return content.encode('ascii','ignore')
            else:
                return page_list[1]

    def parse(self, response):

        reviews=response.xpath('//div[@class="wrap"]')

        for review in reviews:
            title=review.xpath('.//div/a/span/text()').extract_first()
            rating=review.xpath('.//div[@class="rating reviewItemInline"]/span/@class').extract_first()
            content=review.xpath('.//p[@class="partial_entry"]/text()').extract_first()
            date_=review.xpath('.//div[@class="rating reviewItemInline"]/span/text()').extract()
            if len(date_)==1:
                if re.search('(ago)$', date_[0]) != None:
                    date=review.xpath('.//div[@class="rating reviewItemInline"]/span/@title').extract_first()
                else:
                    date=date_[0]
            else:
                date=review.xpath('.//div[@class="rating reviewItemInline"]/span/@title').extract_first()


            categories=review.xpath('.//div[@class="allLabels"]')

            for category in categories:
                if len(category.xpath('.//span/text()').extract())==3:
                    route=category.xpath('.//span/text()').extract()[0]
                    cabin=category.xpath('.//span/text()').extract()[1]
                    destination=category.xpath('.//span/text()').extract()[2]
                else:
                    if len(category.xpath('.//span/text()').extract())==2:
                        route=category.xpath('.//span/text()').extract()[0]
                        cabin='NA'
                        destination=category.xpath('.//span/text()').extract()[1]

                item=TripAdvisorAirlineItem()
                item['title']=title
                item['rating']=rating
                item['date']=date
                item['content']=content
                item['route']=route
                item['cabin']=cabin
                item['destination']=destination

                yield item

            next_page=response.xpath('//div[@class="unified pagination "]/a/@href').extract()
            next_page=self.verify(next_page)
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield Request(next_page, callback=self.parse)
