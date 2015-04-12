# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class XrimaItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    date = Field()
    area = Field()
    image = Field()
    pass

class StockItem(Item):
	ticker = Field()
	value = Field()
	name = Field()
	change = Field()
	volume = Field()