# -*- coding: utf-8 -*-
import traceback
import MySQLdb

class SpiderGoodreadsPipeline(object):
    cc = '''INSERT IGNORE into soider1(title,bookUrl,authorName,authorNameUrl,Illustrator,IllustratorUrl,coverPic,Rating_details,score,ratings,reviews,bookFormat,Published_Time,genres,First_Published_Time,pages,Original_title,Literary_Awards,ISBN,ISBN13,Edition_Language,description)value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    conn = MySQLdb.connect(
        host='127.0.0.1',
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
                item['bookUrl'],
                item['authorName'],
                item['authorNameUrl'],
                item['Illustrator'],
                item['IllustratorUrl'],
                item['coverPic'],
                item['Rating_details'],
                item['score'],
                item['ratings'],
                item['reviews'],
                item['bookFormat'],
                item['Published_Time'],
                item['genres'],
                item['First_Published_Time'],
                item['pages'],
                item['Original_title'],
                item['Literary_Awards'],
                item['ISBN'],
                item['ISBN13'],
                item['Edition_Language'],
                item['description']
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