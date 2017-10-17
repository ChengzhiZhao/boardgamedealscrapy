import pymongo

from scrapy.conf import settings

class BoardgamedealscrapyPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]


    def insert_item(self, item):
        self.collection.insert(dict(item))
        return item
