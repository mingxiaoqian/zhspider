# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request


class ChinaSarft(CrawlSpider):
    name = "chinasarft"

    start_urls = [
        'http://dy.chinasarft.gov.cn/shanty.deploy/catalog.nsp?id=0129dffcccb1015d402881cd29de91ec']

    rules = [
        Rule(LinkExtractor(allow=('id=0129dffcccb1015d402881cd29de91ec',))),
        # Rule(LinkExtractor(allow=('templateId=0129f8148f650065402881cd29f7df33',)), callback='parse_item', follow=True),
    ]


    def parse_item(self, response):
        print(str(response.url))

        # selector = Selector(response)
        # boxcontent = selector.xpath("//div[contains(@class, 'cc boxcontent')]")
        # print(len(boxcontent))
        # tables = selector.xpath("//div[re:match(@id, 'divf')]/table")
        # title = str(selector.xpath("//div[contains(@class, 'heading')]/text()").extract()[0])
        #
        # if not title in self.__pages:
        #     self.__pages[title] = 0
        # else:
        #     print(title)
        #     self.__pages[title] += 1
