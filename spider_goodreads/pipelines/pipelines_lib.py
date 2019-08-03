# -*- coding: utf-8 -*-
import traceback
import MySQLdb
import xlwt
from openpyxl import Workbook


class SpiderGoodreadsPipelineCSV(object):

    cc = '''INSERT IGNORE p_news_lib1(title,state,city,abbreviation,zipcode,email,website,worldcatUrl,address,phone)
    value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    conn = MySQLdb.connect(
        host='120.27.218.142',
        port=3306,
        user='worker',
        passwd='worker',
        db='test',
        charset="utf8"
    )
    cur = conn.cursor()

    def process_item(self, item, spider):
        try:
            insertdata = (
                item['title'],
                item['state'],
                item['city'],
                item['title'],
                item['abbreviation'],
                item['zipcode'],
                item['email'],
                item['website'],
                item['worldcatUrl'],
                item['address'],
                item['phone']
                )
            # print "------insert success-------", insertdata

            self.cur.execute(self.cc, insertdata)
            self.conn.commit()
        except Exception as errinfo:
            traceback.print_exc()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()