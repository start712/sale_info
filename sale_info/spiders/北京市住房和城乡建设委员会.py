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
    name = "000001"

    def start_requests(self):
        url = "http://www.bjjs.gov.cn/bjjs/fwgl/fdcjy/fwjy/index.shtml"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
        item = sale_info.items.SaleInfoItem()
        item['monitor_id'] = self.name
        item['city'] = "北京"
        item['date'] = datetime.datetime.date(datetime.datetime.now())

        try:
            e_div = bs_obj.find('div', id='nr_box')
            e_table = e_div.find_all('table')[1]
            l = pd.read_html(str(e_table), encoding='utf8')
            df1 = l[4]
            df2 = l[-1]

            """
            e_tr1 = e_table.find('tr')
            e_tr2 = list(e_tr1.next_siblings)[-1]

            e_table01 = e_tr1.find_all('td')[-1].table
            e_table02 = e_tr2.find_all('td')[-1].table
            data01, data02 = e_table01.find_all('tr')[1:3]
            data03, data04 = e_table02.find_all('tr')[1:3]
            """
            item['set_count'] = float(df1.loc[1,1]) + float(df2.loc[1,1])
            item['area'] = float(df1.loc[2,1]) + float(df2.loc[2,1])

            yield item
        except:
            log_obj.update_error("%s中无法解析\n原因：%s" %(self.name, traceback.format_exc()))

if __name__ == '__main__':
    pass