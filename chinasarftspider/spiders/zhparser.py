# -*- coding: utf-8 -*-


from scrapy.selector import Selector
from chinasarftspider.items import ChinasarftspiderItem
from chinasarftspider.items import check_new_url


class ZhParser:
    def __init__(self, url):
        self.__item_statistics = {
            'total': 0,
            'right': 0,
            'wrong': 0,
        }
        self.url = url

    def check_and_update_period(self, period, dtime):
        try:
            xlist = period.split("年")
            year = dtime.split(':')[1].split('-')[0]
            if year == xlist[0]:
                return period
            xlist[0] = "%s年" % year
            print("update period ", period, '->', ''.join(xlist))
            return ''.join(xlist)
        except:
            print("check and update period fail,", period, dtime)
            return period

    def parse_item(self, response):
        # print(str(response.url))

        selector = Selector(response)

        try:
            title = selector.xpath("//div[contains(@class, 'heading')]/text()").extract()[0]
            period = title.split("关于")[1].split("全国")[0]
        except:
            period = "unknown"

        try:
            dtime = selector.xpath("//div[contains(@class, 'time')]/ul/li/text()").extract()[0]
            if period in ['2011年06月（下旬）']:
                period = self.check_and_update_period(period, dtime)
        except:
            pass

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

                wrong_list = []

                item = ChinasarftspiderItem()

                i = 2
                td_list = row.xpath("td[%d]/a/text()" % i).extract()
                if len(td_list) > 0:
                    item['case_no'] = td_list[0]
                else:
                    wrong_list.append(tableheader[i - 1])

                td_list = row.xpath("td[%d]/a/@onclick" % i).extract()
                if len(td_list) > 0:
                    item["case_url"] = self.url + td_list[0].split("'")[1]
                else:
                    wrong_list.append(tableheader[i - 1])

                i = 3
                td_list = row.xpath("td[%d]/text()" % i).extract()
                if len(td_list) > 0:
                    item['name'] = td_list[0]
                else:
                    wrong_list.append(tableheader[i - 1])

                i = 4
                td_list = row.xpath("td[%d]/text()" % i).extract()
                if len(td_list) > 0:
                    item['filling_unit'] = td_list[0]
                else:
                    wrong_list.append(tableheader[i - 1])

                i = 5
                td_list = row.xpath("td[%d]/text()" % i).extract()
                if len(td_list) > 0:
                    item['author'] = td_list[0]
                else:
                    wrong_list.append(tableheader[i - 1])

                i = 6
                td_list = row.xpath("td[%d]/text()" % i).extract()
                if len(td_list) > 0:
                    item['result'] = td_list[0]
                else:
                    wrong_list.append(tableheader[i - 1])

                i = 7
                td_list = row.xpath("td[%d]/text()" % i).extract()
                if len(td_list) > 0:
                    if tableheader[6] == "备案地":
                        item['region'] = td_list[0]
                    elif tableheader[6] == "备案时间":
                        item['case_time'] = td_list[0]
                else:
                    wrong_list.append(tableheader[i - 1])

                item["case_type"] = case_type
                item["path_url"] = response.url
                item["period"] = period

                self.process_total_item()
                if len(wrong_list) > 0:
                    self.process_wrong_item(response, row.extract(), wrong_list)
                else:
                    self.process_right_item()

                yield item

    def process_wrong_item(self, response, content, desc):
        print(response.url)
        print(content)
        print("fail to parse ", desc)
        self.__item_statistics['wrong'] += 1

    def process_right_item(self):
        self.__item_statistics['right'] += 1

    def process_total_item(self):
        self.__item_statistics['total'] += 1

    def print_statistics(self):
        for k in self.__item_statistics:
            print(k, ":", self.__item_statistics[k])
