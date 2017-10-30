# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SaleInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    area = scrapy.Field()
    city = scrapy.Field()
    set_count = scrapy.Field()
    monitor_id = scrapy.Field()
    sql_key = scrapy.Field()
    date = scrapy.Field()
    remark = scrapy.Field()
