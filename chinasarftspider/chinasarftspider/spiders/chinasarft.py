# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from chinasarftspider.items import ChinasarftspiderItem
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

    error_count = 0

    def close(self, reason):
        print("total error item count %d" % self.error_count)

    def parse_item(self, response):
        if not check_new_url(response.url):
            return
        # print(str(response.url))

        selector = Selector(response)
        boxcontent = selector.xpath("//div[contains(@class, 'cc boxcontent')]")
        typetable = boxcontent.xpath("//div[contains(@class, 'ta1')]/ul/li/span/text()").extract()
        # print(len(typetable))
        # print(typetable)

        tables = boxcontent.xpath("//div[re:match(@id, 'divf')]/table")
        # print(len(tables))

        idx = 0
        for table in tables:
            case_type = typetable[idx]
            idx += 1

            headrow = True
            rows = table.xpath("tr")
            for row in rows:
                if headrow:
                    tableheader = row.xpath("th/text()").extract()
                    headrow = False
                    continue

                item = ChinasarftspiderItem()

                i = 2
                td_list = row.xpath("td[%d]/a/text()" % i).extract()
                if len(td_list) > 0:
                    item['case_no'] = td_list[0]
                else:
                    self.process_wrong_item(response, row.extract(), tableheader[i - 1])

                td_list = row.xpath("td[%d]/a/@onclick" % i).extract()
                if len(td_list) > 0:
                    item["case_url"] = self.url + td_list[0].split("'")[1]
                else:
                    self.process_wrong_item(response, row.extract(), tableheader[i - 1])

                i += 1
                td_list = row.xpath("td[%d]/text()" % i).extract()
                if len(td_list) > 0:
                    item['name'] = td_list[0]
                else:
                    self.process_wrong_item(response, row.extract(), tableheader[i - 1])

                i += 1
                td_list = row.xpath("td[%d]/text()" % i).extract()
                if len(td_list) > 0:
                    item['filling_unit'] = td_list[0]
                else:
                    self.process_wrong_item(response, row.extract(), tableheader[i - 1])

                i += 1
                td_list = row.xpath("td[%d]/text()" % i).extract()
                if len(td_list) > 0:
                    item['author'] = td_list[0]
                else:
                    self.process_wrong_item(response, row.extract(), tableheader[i - 1])

                i += 1
                td_list = row.xpath("td[%d]/text()" % i).extract()
                if len(td_list) > 0:
                    item['result'] = td_list[0]
                else:
                    self.process_wrong_item(response, row.extract(), tableheader[i - 1])

                i += 1
                td_list = row.xpath("td[%d]/text()" % i).extract()
                if len(td_list) > 0:
                    if tableheader[6] == "备案地":
                        item['region'] = td_list[0]
                    elif tableheader[6] == "备案时间":
                        item['case_time'] = td_list[0]
                else:
                    self.process_wrong_item(response, row.extract(), tableheader[i - 1])

                item["case_type"] = case_type
                item["path_url"] = response.url

                yield item

    def process_wrong_item(self, response, content, desc):
        print(response.url)
        print(content)
        print("fail to parse %s" % desc)
        self.error_count += 1
