# -*- coding: utf-8 -*-
import traceback
import MySQLdb

class SpiderGoodreadsPipeline(object):
    '''
    保存到mysql
    '''
    cc = '''INSERT IGNORE p_news_goodreads2(cudosid,goodreadsId,goodreadsUrl,title,authorName,authorNameUrl,
    Illustrator,IllustratorUrl,coverPic,ratingDetails,score,ratings,reviews,genres,bookFormat,publishedTime,
    firstPublishedTime,pages,originalTitle,literaryAwards,ISBN,ISBN13,editionLanguage,description,isbnInfo)
    value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
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
                item['cudosid'],
                item['goodreadsId'],
                item['goodreadsUrl'],
                item['title'],
                item['authorName'],
                item['authorNameUrl'],
                item['Illustrator'],
                item['IllustratorUrl'],
                item['coverPic'],
                item['ratingDetails'],
                item['score'],
                item['ratings'],
                item['reviews'],
                item['genres'],
                item['bookFormat'],
                item['publishedTime'],
                item['firstPublishedTime'],
                item['pages'],
                item['originalTitle'],
                item['literaryAwards'],
                item['ISBN'],
                item['ISBN13'],
                item['editionLanguage'],
                item['description'],
                item['isbnInfo']
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