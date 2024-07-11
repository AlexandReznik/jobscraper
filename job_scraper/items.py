import scrapy


class JobScraperItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    date_posted = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()