# -*- coding: utf-8 -*-
import traceback
import MySQLdb
'''
item["OriginalUrl"]=response.url
                item["libUrl"]=url.replace("amp;","")
                item["libName"]=name
                item["city"]=info[0]
                item["CA"]=info1[1]
                item["postal"]=info1[2]
                item["Country"]=info1[3]
'''
class SpiderGoodreadsPipeline(object):
    cc = '''INSERT IGNORE into library1(OriginalUrl,libUrl,libName,city,CA,postal,Country)value(%s,%s,%s,%s,%s,%s,%s)'''
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
                item['OriginalUrl'],
                item['libUrl'],
                item['libName'],
                item['city'],
                item['CA'],
                item['postal'],
                item['Country']
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