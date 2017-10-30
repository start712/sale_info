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
    name = "000005"

    headers = {'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive'
            }

    def start_requests(self):
        url = "http://www.njhouse.com.cn/2016/spf/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        driver = PhantomJS_driver.initialization()
        #bs_obj = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        item = sale_info.items.SaleInfoItem()
        item['monitor_id'] = self.name
        item['city'] = "南京"
        item['date'] = datetime.datetime.date(datetime.datetime.now())
        item['set_count'] = ''

        try:
            while not item['set_count']:
                print "爬取000005南京中"
                driver.get(response.url)
                time.sleep(6)
                #e_table = bs_obj.find('div', class_='spf_right')
                item['set_count'] = driver.find_element_by_xpath('//*[@id="todaynum2"]').text#float(e_table.find('span', id = 'todaynum1').get_text(strip=True))
                item['area'] = ''#e_table.find('strong', id = 'todaynum2').get_text(strip=True)

            yield item
        except:
            log_obj.update_error("%s中无法解析\n原因：%s" %(self.name, traceback.format_exc()))

        driver.close()

if __name__ == '__main__':
    pass