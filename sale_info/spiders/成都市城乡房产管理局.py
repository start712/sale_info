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

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
sys.path.append(os.getcwd()) #########
reload(sys)
sys.setdefaultencoding('utf8')
import spider_log  ########

log_obj = spider_log.spider_log() #########

class Spider(scrapy.Spider):
    name = "000004"

    def start_requests(self):
        url = "http://www.cdfgj.gov.cn/SCXX/Default.aspx"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
        item = sale_info.items.SaleInfoItem()
        item['monitor_id'] = self.name
        item['city'] = "成都"
        item['date'] = datetime.datetime.date(datetime.datetime.now())

        try:
            e_table = bs_obj.find('table', class_='blank')
            e_trs = e_table.find_all('tr')[2:]
            data_l = [float(e_tr.find_all('td')[1].get_text(strip=True)) for e_tr in e_trs]

            item['set_count'] = ""
            item['area'] = sum(data_l)

            yield item
        except:
            log_obj.update_error("%s中无法解析\n原因：%s" %(self.name, traceback.format_exc()))

if __name__ == '__main__':
    pass