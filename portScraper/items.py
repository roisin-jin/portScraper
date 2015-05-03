# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CountryItem(Item):
    code = Field()
    name = Field()

class PolygonItem(Item):
    lat = Field()
    lon = Field()

class LocodeItem(Item):
    country = Field()
    port = Field()

class PortscraperItem(Item):
    # define the fields for your item here like:
    name = Field()
    locode = Field()
    polygon = Field()

