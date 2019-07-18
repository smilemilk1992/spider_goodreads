# -*- coding: utf-8 -*-
import traceback
import MySQLdb
'''
item["goodreadsId"] = response.meta['goodreadsId']
        item["relationId"] = response.meta["id"]
        item["goodreadsUrl"] = response.meta['goodreadsUrl']
        item["title"] = response.meta['title']
        item["goodreadsAmazonUrl"] = response.meta['goodreadsAmazonUrl']
        item["amazonUrl"] = response.meta['amazonUrl']
        item["goodreadsAlibrisUrl"] = response.meta['goodreadsAlibrisUrl']
        item["alibrisUrl"] = alibrisUrl
        item["goodreadsWalmarteBooksUrl"] = response.meta['goodreadsWalmarteBooksUrl']
        item["walmarteBooksUrl"] = response.meta['walmarteBooksUrl']
        item["goodreadsBarnesNoble"] = response.meta['goodreadsBarnesNoble']
        item["barnesNoble"] = response.meta['barnesNoble']
'''
class SpiderGoodreadsPipeline(object):
    cc = '''INSERT IGNORE into p_news_snapshot1(goodreadsId,relationId,goodreadsUrl,title,goodreadsAmazonUrl,amazonUrl,goodreadsAlibrisUrl,alibrisUrl,goodreadsWalmarteBooksUrl,walmarteBooksUrl,goodreadsBarnesNoble,barnesNoble)value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
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
                item['goodreadsId'],
                item['relationId'],
                item['goodreadsUrl'],
                item['title'],
                item['goodreadsAmazonUrl'],
                item['amazonUrl'],
                item['goodreadsAlibrisUrl'],
                item['alibrisUrl'],
                item['goodreadsWalmarteBooksUrl'],
                item['walmarteBooksUrl'],
                item['goodreadsBarnesNoble'],
                item['barnesNoble'],
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