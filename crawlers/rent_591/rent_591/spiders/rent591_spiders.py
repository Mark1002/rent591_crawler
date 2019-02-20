"""Rent591 spiders."""
import json
import scrapy
from ajilog import logger


class Rent591Spider(scrapy.Spider):
    """Rent591 spiders class."""

    name = "rent591"

    def start_requests(self):
        page_num = 10
        cookies_mapping = {
            '台北市': 1,
            '新北市': 3,
        }
        for k in cookies_mapping.keys():
            for page in range(page_num):
                url = f'https://rent.591.com.tw/home/search/rsList?is_new_list=1&region={cookies_mapping[k]}&type=1&kind=0&searchtype=1&shType=list&firstRow={page*30}' # noqa
                request = scrapy.Request(
                    url=url,
                    cookies={'urlJumpIp': cookies_mapping[k]},
                    callback=self.parse_house_id
                )
                request.meta['city'] = k
                yield request

    def parse_house_id(self, response):
        res = json.loads(response.body.decode("utf-8"))
        house_ids = [el['houseid'] for el in res['data']['data']]
        logger.debug(house_ids)
        for house_id in house_ids:
            detail_url = f'https://rent.591.com.tw/rent-detail-{house_id}.html'
            request = scrapy.Request(
                url=detail_url,
                callback=self.parse_detail
            )
            request.meta['city'] = response.meta['city']
            request.meta['house_id'] = house_id
            yield request

    def parse_detail(self, response):
        logger.debug(f"city:{response.meta['city']}")
        logger.debug(f"id:{response.meta['house_id']}")
        phone_number = response.css('.dialPhoneNum::attr(data-value)').get()
        logger.debug(phone_number)
