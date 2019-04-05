# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
mkt_db = client['IPO']


class IpoPipeline(object):

  def process_item(self, item, spider):
    col_name = item['uptick_name']
    if item['error']:
      mkt_db[col_name + '_error_urls'].insert_one(item)
    else:
      mkt_db[col_name].insert_one(item)
    return item

  def close_spider(self, spider):
    client.close()


