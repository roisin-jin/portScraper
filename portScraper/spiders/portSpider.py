import re
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from portScraper.items import PortscraperItem, PolygonItem, LocodeItem, CountryItem

class CountrySpider(Spider):
	name = 'country_spider'
	allowed_domains = ['nationsonline.org']
	start_urls = ['http://www.nationsonline.org/oneworld/country_code_list.htm']

	def parse(self, response):

		def process(stx):
			patter = re.compile('>[\w\s(),*\'-]+<')
			return patter.search(stx.encode("utf-8").decode('unicode_escape').encode('ascii','ignore')).group().replace('>', '').replace('<', '').replace('*', '').strip()

		rows = response.xpath('//td[re:test(text(), "[A-Z]{2}")]/parent::tr').extract()

		for row in rows:
			i = CountryItem()
			tds = row.splitlines()
			i["code"] = process(tds[3])
			i["name"] = process(tds[2])

			yield i

class PortSpider(Spider):
	name = 'port_spider'
	allowed_domains = ['unece.org']
	start_urls = ['http://www.unece.org/cefact/locode/service/location.html']

	def __init__(self):
		self.locode_seen = set()

	def parse(self, response):
		links = response.xpath('//a[re:test(@href, "^.+fileadmin/DAM/cefact/locode/[a-z]{2}.htm$")]//@href').extract()
		for link in links:
			actualLink = "http://www.unece.org/" + link.replace("/../", "")
			yield Request(actualLink, self.parse_table)

	def parse_table(self, response):
		rows = response.xpath('//td[re:test(text(), "1(\d|-){7}")]/parent::tr').extract()

		def process(stx): 
			patter = re.compile('<td.*">')
			return patter.sub('', stx.encode("utf-8").decode('unicode_escape').encode('ascii','ignore')).replace('</td>', '').strip()

		def deal(stx, po):
			stp = stx.encode("utf-8")
			return stp[:po] + '.' + stp[po:]

		direction = re.compile('[NEWS]')
		for row in rows:
			i = PortscraperItem()
			tds = row.splitlines()

			i["name"] = process(tds[3])
			locode = process(tds[2])
			if locode in self.locode_seen: continue
			else: self.locode_seen.add(locode)
			
			locodeItem = LocodeItem()
			locodeItem["country"] = locode[:2]
			locodeItem["port"] = locode[2:]
			i["locode"] = dict(locodeItem)

			polygon =  process(tds[10]).split()

			if polygon:
				polyItem = PolygonItem()
				x = float(direction.sub('', deal(polygon[0], 2)))
				if polygon[0].endswith('S'): x = 0 - x
				polyItem["lat"] = x

				y = float(direction.sub('', deal(polygon[1], 3)))
				if polygon[1].endswith('W'): y = 0 - y
				polyItem["lon"] = y

				i["polygon"] = dict(polyItem)

			yield i
