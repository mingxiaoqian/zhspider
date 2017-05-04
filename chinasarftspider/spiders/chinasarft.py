# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.spider import iterate_spider_output
from .zhparser import ZhParser
from chinasarftspider.items import check_new_url

class ChinaSarft(CrawlSpider):
    name = "chinasarft"

    start_urls = [
        'http://dy.chinasarft.gov.cn/shanty.deploy/catalog.nsp?id=0129dffcccb1015d402881cd29de91ec']

    url = 'http://dy.chinasarft.gov.cn'

    rules = [
        Rule(LinkExtractor(allow=('id=0129dffcccb1015d402881cd29de91ec',))),
        Rule(LinkExtractor(allow=('templateId=0129f8148f650065402881cd29f7df33',)), callback='parse_item', follow=True),
    ]

    __zhparser = ZhParser(url)

    def close(self, reason):
        self.__zhparser.print_statistics()

    def parse_item(self, response):
        if not check_new_url(response.url):
            print("skip ---> %s" % response.url)
            return

        res = self.__zhparser.parse_item(response)
        for requests_or_item in iterate_spider_output(res):
            yield requests_or_item
