import scrapy
from urllib.parse import urlparse, parse_qs

class OlxSpider(scrapy.Spider):
    name = 'olx'
    
    start_urls = ['https://www.olx.in/chennai/cars/q-car/?search%5Bdescription%5D=1',
                  'https://www.olx.in/chennai/bikes/']
    def parse(self, response):
        items = response.xpath('//table[@id="offers_table"]//td[contains(@class, "offer onclick")]')
        for t in items:
            product_name = t.xpath('.//a[contains(@class, "detailsLink")]/span/text()').extract_first()
            product_link = t.xpath( './/a[contains(@class, "detailsLink")]/@href' ).extract_first()
            product_price = t.xpath('.//p[contains(@class, "price")]/strong/text()').extract_first()
            product_price = product_price and product_price.strip()
            parsed_url = urlparse('https://www.olx.in/chennai/bikes/?page=2')
            page_no = parse_qs(parsed_url.query).get('page', [1])[0]
            result = {
                'product_name': product_name,
                'product_link': product_link,
                'product_price': product_price,
                'page_number': page_no 
            }
            yield result
        yield {'url': response.url}
        next_page_link = response.xpath( '//a[contains(@class, "pageNextPrev") and ./span/text()="Next page »"]/@href' ).extract_first()
        if next_page_link:
            yield scrapy.Request(response.urljoin(next_page_link), callback=self.parse)
