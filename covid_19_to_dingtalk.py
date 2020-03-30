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

# 解决 python2 中文报错
reload(sys)
sys.setdefaultencoding('utf8')
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 数据库配置
db_config = {
        'host': '61.149.146.136',
        'port': 63306,
        'user': 'clsn',
        'password': '123456',
        'db': 'clsn',
        'charset': 'utf8'
    }

def to_dingtalk():
    # 请求的URL，WebHook地址
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=9f54eaaa734cdab863149bfff2b2fa1be86ea2ec5eb89cad6bf93e7c6b771066"
    #构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    #构建请求数据
    message = {
    "actionCard": {
        "title": title,
        "text": text,
        "hideAvatar": "0",
        "btnOrientation": "0"
    },
    "msgtype": "actionCard"
    }
    #对请求的数据进行json封装
    message_json = json.dumps(message)
    # print message_json
    #发送请求
    info = requests.post(url=webhook,data=message_json,headers=header)
    #打印返回的结果
    print(info.text)

def get_now_info():
    with pymysql.connect(**db_config) as curr:
        sql1 = "select max(monitor_time) from covid_19_overseas"
        curr.execute(sql1)
        date_time = list(curr.fetchone())
        # print date_time[0]

        img = "![screenshot](https://cdn.nlark.com/yuque/0/2020/png/206952/1585575860917-569c54c2-84db-4c45-ad35" \
              "-0a96455a90bc.png)\n"
        head = "## <font color=#FFBF00>[风险提示]</font> <font color=#000000>全球新型冠状病毒肺炎疫情</font>\n"
        msg_from = '\n >数据更新至 {}'.format(date_time[0])

        sql2 = "select sum(confirm) as '累计确诊',sum(heal) as '治愈',sum(confirmCompare) as '新增确诊',sum(dead) as '死亡' from " \
               "covid_19_overseas where monitor_time = '{}' ".format(date_time[0])
        curr.execute(sql2)
        data = list(curr.fetchone())
        bf_dead = round(data[3]/data[0]*100,2)
        bf_heal = round(data[1]/data[0]*100,2)
        info = """\n ## **确诊病例:** <font color=#FF0000>{}</font>
                   \n ## **死亡病例:** <font color=#404040>{} ({}%)</font>
	               \n ## **治愈病例:** <font color=#9DEA15> {} ({}%)</font>
	               \n ## **新增病例:** <font color=#FFBF00> {}</font>\n""" .format(format(data[0],','),
                                                                             format(data[3],','),bf_dead,
                                                                             format(data[1],','),bf_heal,
                                                                             format(data[2],','))

        sql3 = "select confirm as '累计确诊', heal as '治愈',confirmCompare as '新增确诊',dead as '死亡',country as '国家' from " \
               "covid_19_overseas where monitor_time = '{}' limit 5;".format(date_time[0])
        curr.execute(sql3)
        top_data = list(curr.fetchall())
        country_info = ''
        for data in top_data:
            # print data
            info_ = """ \n -国家：{} 
                               \n ## **确诊病例:** <font color=#FF0000>{}</font>
                               \n ## **死亡病例:** <font color=#404040>{}</font>
            	               \n ## **治愈病例:** <font color=#9DEA15> {}</font>
            	               \n ## **新增病例:** <font color=#FFBF00> {}</font>\n *** \n """.format(data[4],
                                                                                          format(data[0], ','),
                                                                                          format(data[3], ','),
                                                                                          format(data[1], ','),
                                                                                          format(data[2], ','))
            country_info = country_info + info_

        talk_all = '\n# *风险等级TOP5*\n'

        to_dingtalk_data = img + head + "***" + info  + "***" + talk_all + "***"  + country_info + msg_from
        return  to_dingtalk_data

if __name__=="__main__":
    title = "新型冠状病毒疫情(国际)实时追踪"
    text = get_now_info()
    to_dingtalk()
