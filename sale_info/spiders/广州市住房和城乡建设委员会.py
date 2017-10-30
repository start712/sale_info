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
import numpy as np

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
sys.path.append(os.getcwd()) #########
reload(sys)
sys.setdefaultencoding('utf8')
import spider_log  ########

log_obj = spider_log.spider_log() #########

class Spider(scrapy.Spider):
    name = "000009"

    def start_requests(self):
        url = "http://www.gzcc.gov.cn/Category_177/Index.aspx"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
        item = sale_info.items.SaleInfoItem()
        item['monitor_id'] = self.name
        item['city'] = "广州"
        item['date'] = datetime.datetime.date(datetime.datetime.now())

        try:
            e_table = bs_obj.find('div', class_='wBd').find_all('table')[-2]
            e_trs = e_table.find_all('tr')[3:]
            # 将表格中的数据保存为二位列表
            data_l = []
            for e_tr in e_trs:
                e_tds = e_tr.find_all('td')[1:]
                row = [float(e_td.get_text(strip=True)) for e_td in e_tds]
                data_l.append(row)

            arr = np.array(data_l)

            item['set_count'] = float(sum(sum([arr[:,i] for i in xrange(10) if i % 2 == 0 and i != 6 ])))
            item['area'] = float(sum(sum([arr[:,i] for i in xrange(10) if i % 2 == 1 and i != 7 ])))

            yield item
        except:
            log_obj.update_error("%s中无法解析\n原因：%s" %(self.name, traceback.format_exc()))

if __name__ == '__main__':
    pass