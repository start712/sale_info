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


sys.path.append(sys.prefix + "\\Lib\\MyWheels")
sys.path.append(os.getcwd()) #########
reload(sys)
sys.setdefaultencoding('utf8')
import spider_log  ########
import PhantomJS_driver
PhantomJS_driver = PhantomJS_driver.PhantomJS_driver()
log_obj = spider_log.spider_log() #########

class Spider(scrapy.Spider):
    name = "000002"

    def start_requests(self):
        url = "http://www.fangdi.com.cn/MarketAnalysis.htm"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        driver = PhantomJS_driver.initialization(web_security='false')
        try:
            driver.get(response.url)
            driver.switch_to.frame('Report')

            bs_obj = bs4.BeautifulSoup(driver.page_source, 'html.parser')
            item = sale_info.items.SaleInfoItem()
            item['monitor_id'] = self.name
            item['city'] = "上海"
            item['date'] = datetime.datetime.date(datetime.datetime.now())

            e_table = bs_obj.body.table
            s = e_table.get_text(strip=True)
            item['set_count'] = re.search(ur'(?<=(今日共预/出售各类商品房))\d+', s).group()
            item['area'] = float(re.search(ur'(?<=(面积))[\d\.]+(?=(万平方米))', s).group()) * 10000

            yield item
        except:
            log_obj.update_error("%s中无法解析\n原因：%s" %(self.name, traceback.format_exc()))

        driver.close()

if __name__ == '__main__':
    pass