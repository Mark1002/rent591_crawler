"""Rent591 spiders."""
import json
import scrapy
from ajilog import logger


class Rent591Spider(scrapy.Spider):
    """Rent591 spiders class."""

    name = "rent591"

    except_list = []

    def start_requests(self):
        page_num = 3
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
        """Parse for house id."""

        res = json.loads(response.body.decode("utf-8"))
        for house_info in res['data']['data']:
            house_id = house_info['houseid']
            renter_type, renter = house_info['nick_name'].split()
            detail_url = f'https://rent.591.com.tw/rent-detail-{house_id}.html'
            request = scrapy.Request(
                url=detail_url,
                callback=self.parse_detail
            )
            request.meta['city'] = response.meta['city']
            request.meta['house_id'] = house_id
            request.meta['renter'] = renter
            request.meta['renter_type'] = renter_type
            yield request

    def parse_detail(self, response):
        """Parse detail house info fields."""
        try:
            city = response.meta['city']
            house_id = response.meta['house_id']
            detail_dict = dict([tuple(
                    ''.join(el.split()).split(':')
                ) for el in response.css(
                    '.detailInfo li::text'
                ).getall()
            ])
            house_type = detail_dict.get('型態', None)
            house_recent = detail_dict.get('現況', None)
            phone_number = response.css(
                '.dialPhoneNum::attr(data-value)').get()
            renter = response.meta['renter']
            renter_sex = 0 if "先生" in renter else 1
            renter_type = response.meta['renter_type']

            rent_condition = response.css(
                '.labelList em::attr(title)').getall()
            if '男生' in rent_condition:
                sex_limit = 0
            elif '女生' in rent_condition:
                sex_limit = 1
            else:
                sex_limit = 2

            rent_info = {
                'house_id': house_id,
                'house_type': house_type,
                'house_recent': house_recent,
                'city': city,
                'renter': renter,
                'renter_sex': renter_sex,
                'renter_type': renter_type,
                'phone_number': phone_number,
                'sex_limit': sex_limit
            }
            yield rent_info
        except Exception as e:
            self.except_list.append({
                'house_id': response.meta['house_id'],
                'message': str(e)
            })
        finally:
            logger.debug(self.except_list)
