import scrapy

class SpiderAmazon(scrapy.Spider):
    name = "spiderAmazon"

    def __init__(self, *args, **kwargs):
        super(SpiderAmazon, self).__init__(*args, **kwargs)

        # Parse URL
        self.start_urls = [kwargs.get('start_url')]
        if self.start_urls == [None]:
            self.start_urls =[
                'https://www.amazon.com/'
            ]

        # Parse max_page
        self.max_page = kwargs.get('max_page')
        if self.max_page:
            self.max_page = int(self.max_page)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'amazon.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)