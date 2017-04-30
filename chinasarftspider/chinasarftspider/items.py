# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import sys
import scrapy
from scrapy_djangoitem import DjangoItem
from screenplay.notebook.models import ScreenPlay

def check_new_url(url):
    qs = ScreenPlay.objects.filter(case_url=url)
    if qs.count() < 1:
        return True
    else:
        return False

class ChinasarftspiderItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = ScreenPlay

