# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: controller.py
    @time: 2017/7/3 16:03
--------------------------------
"""
import sys
import os

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')
import set_log  # log_obj.debug(文本)  "\x1B[1;32;41m (文本)\x1B[0m"

log_obj = set_log.Logger('controller.log', set_log.logging.WARNING,
                         set_log.logging.DEBUG)
log_obj.cleanup('controller.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


class controller(object):
    def __init__(self):
        pass

    def run_scrapy(self):
        os.system('scrapy sale_info')

if __name__ == '__main__':
    controller = controller()
    controller.run_scrapy()