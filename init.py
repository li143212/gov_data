# -*- coding: utf-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
import sqlite3
DOMTree = xml.dom.minidom.parse(open("坪山区-民生诉求数据_完整版.xml", encoding='utf8'))
k = ['REC_ID',	'REPORT_NUM',	'CREATE_TIME',	'DISTRICT_NAME',	'DISTRICT_ID',	'STREET_NAME',	'STREET_ID',	'COMMUNITY_NAME',	'COMMUNITY_ID',	'EVENT_TYPE_NAME',	'EVENT_TYPE_ID',	'MAIN_TYPE_NAME',	'MAIN_TYPE_ID',	'SUB_TYPE_NAME',	'SUB_TYPE_ID',	'DISPOSE_UNIT_NAME',	'DISPOSE_UNIT_ID',	'EVENT_SRC_NAME',	'EVENT_SRC_ID',	'OPERATE_NUM',	'OVERTIME_ARCHIVE_NUM',	'INTIME_TO_ARCHIVE_NUM',	'INTIME_ARCHIVE_NUM',	'EVENT_PROPERTY_ID',	'EVENT_PROPERTY_NAME',	'OCCUR_PLACE']
collection = DOMTree.documentElement
ll = []
for name in k:
    ll.append(collection.getElementsByTagName(name))
object_list = zip(*ll)
conn = sqlite3.connect('datatest.db')
cursor = conn.cursor()
for o in object_list:
    data = list(map(lambda x:'"%s"'%x.childNodes[0].data,o))
    sql = "insert into data (%s) values (%s)" % (",".join(k),",".join(data))
    print(sql)
    cursor.execute(sql)

print('rowcount =', cursor.rowcount)
# 关闭Cursor:
cursor.close()
# 提交事务:
conn.commit()
# 关闭Connection:
conn.close()