"""Rent591 data pipelines."""
import pymongo
from ajilog import logger


class Rent591Pipeline(object):
    """Item data save to mongoDB."""

    collection_name = 'rents'

    def __init__(self, db_uri, db_name):
        """init."""
        self.db_uri = db_uri
        self.db_name = db_name

    @classmethod
    def from_crawler(cls, crawler):
        """Get crawler global settings."""
        return cls(
            db_uri=crawler.settings.get('MONGO_URI'),
            db_name=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        """Open spider."""
        self.client = pymongo.MongoClient(self.db_uri)
        self.db = self.client[self.db_name]
        # for mongoDB string index
        self.db[self.collection_name].create_index([
            ('$**', pymongo.TEXT)
        ])
        # create unique key on house id
        self.db[self.collection_name].create_index([
            ('house_id', pymongo.ASCENDING)], unique=True)

    def close_spider(self, spider):
        """Close spider."""
        self.client.close()

    def process_item(self, item, spider):
        """Save item to db."""
        try:
            self.db[self.collection_name].insert_one(dict(item))
        except Exception as e:
            logger.debug(str(e))
        return item
