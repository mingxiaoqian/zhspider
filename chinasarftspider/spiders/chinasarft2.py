# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.spider import iterate_spider_output
from .zhparser import ZhParser
from chinasarftspider.items import check_new_url

class ChinaSarft2(Spider):
    name = "chinasarft2"

    start_urls = [
        'http://dy.chinasarft.gov.cn/shanty.deploy/catalog.nsp?id=0129dffcccb1015d402881cd29de91ec']

    def __init__(self):
        self.url = 'http://dy.chinasarft.gov.cn'
        self.__zhparser = ZhParser(self.url)

    def close(self, reason):
        self.__zhparser.print_statistics()

    def parse(self, response):
        selector = Selector(response)
        articles = selector.xpath("//ul/li/a[re:match(@href, 'templateId=0129f8148f650065402881cd29f7df33')]/@href")

        # print(len(articles))
        for article in articles.extract():
            # print(article)
            article_url = self.url + str(article)
            if check_new_url(article_url):
                yield Request(article_url, callback=self.__zhparser.parse_item)
            else:
                print("skip ---> %s" % article_url)

        next_link = selector.xpath("//a[contains(.//text(), '下一页')]/@href").extract()
        if len(next_link) == 1:
            next_link = self.url + str(next_link[0])
            yield Request(next_link, callback=self.parse)

