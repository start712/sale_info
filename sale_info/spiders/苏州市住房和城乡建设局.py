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
    name = "000007"

    headers = {'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive'
            }


    def start_requests(self):
        url = "http://www.szjsj.gov.cn/ZhuJian/NewAction_property.action"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        desired_capabilities = selenium.webdriver.DesiredCapabilities.PHANTOMJS.copy()

        for key, value in self.headers.iteritems():
            desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
        desired_capabilities['phantomjs.page.customHeaders.User-Agent'] ='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

        driver = selenium.webdriver.PhantomJS(desired_capabilities=desired_capabilities)

        driver.get(response.url)
        driver.switch_to.frame(0)

        bs_obj = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        item = sale_info.items.SaleInfoItem()
        item['monitor_id'] = self.name
        item['city'] = "苏州"
        item['date'] = datetime.datetime.date(datetime.datetime.now())

        try:
            e_marquee = bs_obj.find('marquee')
            s = e_marquee.get_text(strip=True)

            item['set_count'] = re.search(ur'(?<=商品房)\d+', s).group()
            item['area'] = re.search(ur'(?<=、)[\d\.]+(?=平方米)', s).group()

            yield item
        except:
            log_obj.update_error("%s中无法解析\n原因：%s" %(self.name, traceback.format_exc()))

        driver.close()

if __name__ == '__main__':
    pass