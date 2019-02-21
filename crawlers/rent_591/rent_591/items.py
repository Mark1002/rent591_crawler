"""Rent591 items."""
import scrapy


class Rent591Item(scrapy.Item):
    """Rent house item."""

    id = scrapy.Field()
    house_id = scrapy.Field()
    house_type = scrapy.Field()
    house_recent = scrapy.Field()
    city = scrapy.Field()
    renter = scrapy.Field()
    renter_type = scrapy.Field()
    renter_sex = scrapy.Field()
    phone_number = scrapy.Field()
    sex_limit = scrapy.Field()
    date_time = scrapy.Field()
