#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# auth: clsn
# by： covid-19
# date 20200328
#**********************

import requests
import json
import pymysql
import datetime
import sys
pymysql.install_as_MySQLdb()
import MySQLdb

# 解决 python2 中文报错
reload(sys)
sys.setdefaultencoding('utf8')
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

db_config = {
        'host': '123.115.204.251',
        'port': 63306,
        'user': 'clsn',
        'password': '123456',
        'db': 'clsn',
        'charset': 'utf8'
    }

'''
数据库说明
1、表结构
+----------------+--------------+------+-----+---------+----------------+
| Field          | Type         | Null | Key | Default | Extra          |
+----------------+--------------+------+-----+---------+----------------+
| id             | int(11)      | NO   | PRI | NULL    | auto_increment |
| country        | varchar(256) | YES  | MUL | NULL    |                |
| confirm        | int(32)      | YES  |     | NULL    |                |
| heal           | int(32)      | YES  |     | NULL    |                |
| confirmCompare | int(32)      | YES  |     | NULL    |                |
| dead           | int(32)      | YES  |     | NULL    |                |
| monitor_time   | varchar(64)  | YES  | MUL | NULL    |                |
+----------------+--------------+------+-----+---------+----------------+
2、建表语句
REATE TABLE `covid_19_overseas` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `country` varchar(256) DEFAULT NULL COMMENT '国家',
  `confirm` int(32) DEFAULT NULL COMMENT '累计确诊',
  `heal` int(32) DEFAULT NULL COMMENT '治愈',
  `confirmCompare` int(32) DEFAULT NULL COMMENT '新增确诊',
  `dead` int(32) DEFAULT NULL COMMENT '死亡',
  `monitor_time` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `country` (`country`(255)),
  KEY `monitor_time` (`monitor_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''

data = requests.get('https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist')
json_format = json.loads(data.text)

values = ''
with pymysql.connect(**db_config) as cur:
    for i in json_format['data']:
        # data source
        # {u'nowConfirm': 100598, u'name': u'\u7f8e\u56fd', u'confirm': 104839, u'heal': 2525, u'confirmCompare':18796, u'nowConfirmCompare': 16612, u'dead': 1716, u'healCompare': 1772, u'isUpdated': True, u'confirmAddCut': 0, u'date': u'03.28', u'suspect': 0, u'confirmAdd': 18794, u'deadCompare': 412, u'continent': u'\u5317\u7f8e\u6d32'}
        country = i['name']
        # 累计确诊
        confirm = i['confirm']
        # 治愈
        heal = i['heal']
        # 新增确诊
        confirmCompare = i['confirmCompare']
        # 死亡
        dead = i['dead']
        sql = 'insert into covid_19_overseas(country,confirm,heal,confirmCompare,dead,monitor_time) value'
        val = "('{}',{},{},{},{},'{}')".format(country,confirm,heal,confirmCompare,dead,now_time)
        ins_sql = sql + val
        cur.execute(ins_sql)
exit('200')