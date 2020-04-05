
# import scrapy


# class PilotSpider(scrapy.Spider):
#     name = "pilot"
#     start_urls = [
#         'https://fr.trustpilot.com/categories/bank',
#     ]


#     def parse(self, response):
#         for review in response.css('article.review'):
#             yield {
#                 'title': review.css('a.link.link--large.link--dark::text').extract_first(),
#                 'content': review.css('p.review-content__text::text').extract_first(),
#                 'author': review.css('div.consumer-information__name::text').extract_first(),
#             }

#         next_page = response.css('a.button.button--primary.next-page::attr(href)').extract_first()
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)

