# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class XiaoshuoPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    collection_name = 'xiaoshuo_all'

    def __init__(self, mongo_uri, mongo_db,mongo_port):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_port = mongo_port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_port=crawler.settings.get('MONGO_PORT')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_uri,port= self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #self.db[self.collection_name].update({'name': item['name'],'chapter': item['chapter']}, dict(item), True)
        self.db[item['name']].update({'name': item['name'],'chapter': item['chapter']}, dict(item), True)
        return item

