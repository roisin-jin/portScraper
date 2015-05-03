import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):

	def __init__(self):
		client = pymongo.MongoClient(settings['MONGODB_URL'])
		db = client['cv-ports-app-db']
		self.collection = db[settings['MONGODB_COLLECTION']]

	def process_item(self, item, spider):
		valid = True

		for data in item:
			if not data:
				valid = False
				raise DropItem("Missing {0}!".format(data))

		if valid:
			self.collection.insert(dict(item))
			log.msg("Port added to MongoDB database!", level=log.DEBUG, spider=spider)

		return item

class MongoDBPipeline2(object):

	def __init__(self):
		client = pymongo.MongoClient(settings['MONGODB_URL'])
		db = client['cv-ports-app-db']
		self.collection = db['ISOCountries']

	def process_item(self, item, spider):
		valid = True

		for data in item:
			if not data:
				valid = False
				raise DropItem("Missing {0}!".format(data))

		if valid:
			self.collection.insert(dict(item))
			log.msg("Port added to MongoDB database!", level=log.DEBUG, spider=spider)

		return item