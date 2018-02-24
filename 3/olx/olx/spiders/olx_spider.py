import scrapy
from urllib.parse import urlparse, parse_qs
from ..items import OlxItem, OlxLoader

class OlxSpiderCars(scrapy.Spider):
    name = 'olx_cars'
    
    start_urls = ['https://www.olx.in/chennai/cars/q-car/?search%5Bdescription%5D=1']
    def parse(self, response):
        items = response.xpath('//table[@id="offers_table"]//td[contains(@class, "offer onclick")]')
        for t in items:
            loadder = OlxLoader(selector=t)
            loadder.add_xpath('product_name', './/a[contains(@class, "detailsLink")]/span/text()')
            loadder.add_xpath('product_link', './/a[contains(@class, "detailsLink")]/@href' )
            loadder.add_xpath('product_price', './/p[contains(@class, "price")]/strong/text()')
            # product_price = product_price and product_price.strip()
            parsed_url = urlparse('https://www.olx.in/chennai/bikes/?page=2')
            page_no = parse_qs(parsed_url.query).get('page', [1])[0]
            loadder.add_value('page_number', 'page_no')
            yield loadder.load_item()

        yield {'url': response.url}
        next_page_link = response.xpath( '//a[contains(@class, "pageNextPrev") and ./span/text()="Next page »"]/@href' ).extract_first()
        if next_page_link:
            yield scrapy.Request(response.urljoin(next_page_link), callback=self.parse)


class OlxSpiderBikes(OlxSpiderCars):
    name = 'olx_bikes'
    start_urls = ['https://www.olx.in/chennai/bikes/']