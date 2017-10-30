# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: proxy_spider.py
    @time: 2017/3/9 16:27
--------------------------------
"""
import sys
import os
import scrapy
import sale_info.items
import re
import datetime
import bs4
import traceback
import pandas as pd
import selenium.webdriver
import time

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
sys.path.append(os.getcwd()) #########
reload(sys)
sys.setdefaultencoding('utf8')
import spider_log  ########
import PhantomJS_driver
PhantomJS_driver = PhantomJS_driver.PhantomJS_driver()

log_obj = spider_log.spider_log() #########

class Spider(scrapy.Spider):
    name = "000010"

    def start_requests(self):
        url = "http://news.0731fdc.com/?mod=list&act=news&catid=135"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        bs_obj = bs4.BeautifulSoup(PhantomJS_driver.get_html(response.url), 'html.parser')
        item = sale_info.items.SaleInfoItem()
        item['monitor_id'] = self.name
        item['city'] = "长沙"
        item['date'] = datetime.datetime.date(datetime.datetime.now())

        try:
            e_table = bs_obj.find('ul', id='jyphb')
            s = e_table.get_text(strip=True)
            item['set_count'] = ""
            item['area'] = float(re.search(ur'(?<=新房供应)[\d\.]+(?=万㎡)', s).group()) * 10000 / 7
            item['remark'] = e_table.font.get_text(strip=True)

            yield item
        except:
            log_obj.update_error("%s中无法解析\n原因：%s" %(self.name, traceback.format_exc()))

if __name__ == '__main__':
    pass