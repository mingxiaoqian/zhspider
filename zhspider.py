#!/usr/bin/env python
# coding=utf-8

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from django.db import connection


def crawl():
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl('chinasarft')
    process.start()
    process.join()
    connection.close()  # NOTE


def crawl2():
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl('chinasarft2')
    process.start()
    process.join()
    connection.close()  # NOTE

#from scrapy import cmdline
#cmdline.execute("scrapy crawl chinasarft".split())
#cmdline.execute("scrapy crawl chinasarft2".split())

if __name__ == '__main__':
    crawl2()
