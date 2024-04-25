# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OsintnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    id = scrapy.Field()
    title = scrapy.Field()
    image_url = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    author = scrapy.Field()
    sentiment = scrapy.Field()
    is_fake = scrapy.Field()
    published_at = scrapy.Field()
    