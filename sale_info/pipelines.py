# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
import re
from twisted.enterprise import adbapi
import sys
import datetime
import os
import json
import copy
import traceback


log_path = r'%s/log/pipelines_error(%s).log' %(os.getcwd(),datetime.datetime.date(datetime.datetime.today()))

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')
import set_log  # log_obj.debug(文本)  "\x1B[1;32;41m (文本)\x1B[0m"

log_obj = set_log.Logger(log_path, set_log.logging.WARNING, set_log.logging.DEBUG)
log_obj.cleanup(log_path, if_cleanup=False)  # 是否需要在每次运行程序前清空Log文件

import logging
import logging.handlers

LOG_FILE = r'%s/log/duplicate_entry(%s).log' %(os.getcwd(),datetime.datetime.date(datetime.datetime.today()))

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
fmt = '%(asctime)s: %(message)s'

formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter

logger0 = logging.getLogger('tst')  # 获取名为tst的logger
logger0.addHandler(handler)  # 为logger添加handler
logger0.setLevel(logging.DEBUG)

class SaleInfoPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        # self.ban_keys = []

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

        # 备用
        #    def get_keys(self, settings):
        #        self.ban_keys = settings['BAN_KEYS']

    # pipeline默认调用
    def process_item(self, item0, spider):
        """
其原因是由于Spider的速率比较快，而scapy操作数据库操作比较慢，导致pipeline中的方法调用较慢，这样当一个变量正在处理的时候，一个新的变量过来，之前的变量的值就会被覆盖
，比如pipline的速率是1TPS，而spider的速率是5TPS，那么数据库应该会有5条重复数据。

解决方案是对变量进行保存，在保存的变量进行操作，通过互斥确保变量不被修改
        """
        try:
            item = copy.deepcopy(item0)
            if 'remark' not in item:
                item['remark'] = ''
            #print item,item
            item['sql_key'] = "%s/%s" %(item["monitor_id"], item["date"])
            query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
            query.addErrback(self._handle_error,item,spider)#调用异常处理方法
            return item
        except:
            log_obj.error(u"process item error\nINFO:%s" % (traceback.format_exc()))

    # 写入数据库中
    def _conditional_insert(self, tx, item):
        sql = "INSERT INTO `sale_info`(`crawler_id`, `key`, `date`, `city`, `area`, `set_count`, `remark`) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        params = (item["monitor_id"], item['sql_key'], item["date"], item['city'], item["area"], item["set_count"], item['remark'])
        try:
            tx.execute(sql, params)
        except pymysql.IntegrityError:
            logger0.info(params)
        except:
            log_obj.error(u"sql insert failed:%s\nINFO:%s" % (item["sql_key"], traceback.format_exc()))
            #t = (item["monitor_id"], item['sql_key'], item["date"], item['city'], item["area"], item["set_count"], item['remark'])
            #log_obj.error("%s" %{s:type(s) for s in t})

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue


if __name__ == '__main__':
    pass
