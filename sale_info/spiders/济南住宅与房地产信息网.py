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
    name = "000008"

    def start_requests(self):
        url = "http://www.jnfdc.gov.cn/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
        item = sale_info.items.SaleInfoItem()
        item['monitor_id'] = self.name
        item['city'] = "济南"
        item['date'] = datetime.datetime.date(datetime.datetime.now())

        try:
            e_table = bs_obj.find('div', id='todayview').find('div', class_='col_bg')
            e_rows = e_table.ul.find_all('ul')
            # 将表格中的数据保存为二位列表
            e_lis = [[float(e_li.get_text(strip=True)) for e_li in e_row.find_all('li') if e_row.find_all('li')
                     .index(e_li)>0] for e_row in e_rows]

            arr = np.array(e_lis)

            item['set_count'] = float(sum(arr[:,0]))
            item['area'] = float(sum(arr[:,1]))

            yield item
        except:
            log_obj.update_error("%s中无法解析\n原因：%s" %(self.name, traceback.format_exc()))

if __name__ == '__main__':
    pass