# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst

class OlxItem(Item):
    # define the fields for your item here like:
    product_name = Field()
    product_link = Field()
    # product_price = Field(input_processor=MapCompose(lambda x: x.strip()))
    product_price = Field()
    page_number = Field()


class OlxLoader(ItemLoader):
	default_item_class = OlxItem
	default_output_processor = TakeFirst()

	product_price_in = MapCompose(lambda x: x.strip())