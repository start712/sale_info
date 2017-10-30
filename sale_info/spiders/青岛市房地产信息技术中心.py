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

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
sys.path.append(os.getcwd()) #########
reload(sys)
sys.setdefaultencoding('utf8')
import spider_log  ########
import PhantomJS_driver
PhantomJS_driver = PhantomJS_driver.PhantomJS_driver()
log_obj = spider_log.spider_log() #########

class Spider(scrapy.Spider):
    name = "000006"

    headers = {'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive'
            }

    def start_requests(self):
        url = "https://www.qdfd.com.cn/qdweb/realweb/fh/fhNewsale.jsp"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        bs_obj = bs4.BeautifulSoup(PhantomJS_driver.get_html(response.url), 'html.parser')
        #log_obj.update_debug(bs_obj.prettify(encoding='utf8'))
        item = sale_info.items.SaleInfoItem()
        item['monitor_id'] = self.name
        item['city'] = "青岛"
        item['date'] = datetime.datetime.date(datetime.datetime.now())

        try:
            e_table = bs_obj.find('table', class_='jrcj_table1')

            e_tr = e_table.find_all('tr', class_=' ysjrcj_table')[2]
            e_tds = e_tr.find_all('td')[1:]
            data_l1 = [e_tds[i].get_text(strip=True) for i in xrange(len(e_tds)) if i % 3 == 0]
            data_l2 = [e_tds[i].get_text(strip=True) for i in xrange(len(e_tds)) if i % 3 == 1]
            data_l1 = [float(s) for s in data_l1]
            data_l2 = [float(s) for s in data_l2]

            item['set_count'] = sum(data_l1)
            item['area'] = sum(data_l2)

            yield item
        except:
            log_obj.update_error("%s中无法解析\n原因：%s" %(self.name, traceback.format_exc()))

        driver.close()

if __name__ == '__main__':
    pass