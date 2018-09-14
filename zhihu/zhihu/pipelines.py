# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from zhihu.settings import MONGO_DB, MONGO_COL


class ZhihuPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, mongo_db, mongo_col):
        self.mongo_db = mongo_db
        self.mongo_col = mongo_col

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_col=crawler.settings.get('MONGO_COL')
        )

    def open_spider(self, spider):
        self.my_client = pymongo.MongoClient()
        self.my_db = self.my_client[self.mongo_db]
        self.my_col = self.my_db[self.mongo_col]

    def process_item(self, item, spider):
        self.my_col.update({'url_token': item['url_token']}, {'$set': dict(item)}, upsert=True)
        return item

    def close_spider(self, spider):
        self.my_client.close()
