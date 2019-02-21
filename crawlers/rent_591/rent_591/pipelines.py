"""Rent591 data pipelines."""
import pymongo


class Rent591Pipeline(object):
    """Item data save to mongoDB."""

    collection_name = 'rents'

    def __init__(self, db_uri, db_name):
        self.db_uri = db_uri
        self.db_name = db_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_uri=crawler.settings.get('MONGO_URI'),
            db_name=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.db_uri)
        self.db = self.client[self.db_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
