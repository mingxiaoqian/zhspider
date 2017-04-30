# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from .items import ChinasarftspiderItem

class ChinasarftspiderPipeline(object):
    def process_item(self, item, spider):
        # print("\t", item["name"])
        try:
            item.save()
        except:
            import traceback
            traceback.print_exc()
            raise DropItem("Item save error: %s" % item['name'])
        return item
