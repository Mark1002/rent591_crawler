"""Rent591 spiders."""
import json
import scrapy
from ajilog import logger


class Rent591Spider(scrapy.Spider):
    """Rent591 spiders class."""

    name = "rent591"

    def start_requests(self):
        pages = 0
        url = f'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&shType=list&firstRow={pages*30}' # noqa
        yield scrapy.Request(
            url=url,
            cookies={'urlJumpIp': 1},
            callback=self.parse_house_id
        )

    def parse_house_id(self, response):
        res = json.loads(response.body.decode("utf-8"))
        house_ids = [el['houseid'] for el in res['data']['data']]
        logger.debug(house_ids)
        for house_id in house_ids:
            detail_url = f'https://rent.591.com.tw/rent-detail-{house_id}.html'
            yield response.follow(detail_url, self.parse_detail)

    def parse_detail(self, response):
        phone_number = response.css('.dialPhoneNum::attr(data-value)').get()
        logger.debug(phone_number)
