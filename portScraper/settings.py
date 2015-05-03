# -*- coding: utf-8 -*-

# Scrapy settings for portScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'portScraper'

SPIDER_MODULES = ['portScraper.spiders']
NEWSPIDER_MODULE = 'portScraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'portScraper (+http://www.yourdomain.com)'
ITEM_PIPELINES = {'portScraper.pipelines.MongoDBPipeline': 300, }

MONGODB_URL = 'mongodb://localhost:27017'
MONGODB_COLLECTION = 'ports'