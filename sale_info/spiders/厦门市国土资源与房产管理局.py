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

log_obj = spider_log.spider_log() #########

class Spider(scrapy.Spider):
    name = "000011"

    headers = {'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive'
            }

    def start_requests(self):
        url = "http://www.xmtfj.gov.cn/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        driver = self.initialization()
        driver.get(response.url)
        driver.find_element_by_xpath('//*[@id="td_52"]').click()
        driver.switch_to.frame(1)

        bs_obj = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        item = sale_info.items.SaleInfoItem()
        item['monitor_id'] = self.name
        item['city'] = "厦门"
        item['date'] = datetime.datetime.date(datetime.datetime.now())

        try:
            e_table = bs_obj.table
            e_trs = e_table.find_all('tr')
            e_tr1 = e_trs[3]
            set_row = [e.get_text(strip=True) for e in e_tr1.find_all('td')][1:]
            e_tr2 = e_trs[4]
            area_row = [e.get_text(strip=True) for e in e_tr2.find_all('td')][1:]
            item['set_count'] = sum([float(s) for s in set_row]) / 10
            item['area'] = sum([float(s) for s in area_row]) / 10
            item['remark'] = '10天均值'

            yield item
        except:
            log_obj.update_error("%s中无法解析\n原因：%s" %(self.name, traceback.format_exc()))

        driver.close()

    def initialization(self):
        # 初始化浏览器
        desired_capabilities = selenium.webdriver.DesiredCapabilities.PHANTOMJS.copy()

        for key, value in self.headers.iteritems():
            desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
        desired_capabilities['phantomjs.page.customHeaders.User-Agent'] ='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

        return selenium.webdriver.PhantomJS(desired_capabilities=desired_capabilities)

if __name__ == '__main__':
    pass