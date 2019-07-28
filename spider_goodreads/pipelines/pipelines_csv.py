# -*- coding: utf-8 -*-
import traceback
import MySQLdb
import xlwt
class SpiderGoodreadsPipelineCSV(object):
    colum = ["cudosid", "goodreadsId", "goodreadsUrl", "title", "authorName", "authorNameUrl", "Illustrator","IllustratorUrl",
             "coverPic","ratingDetails","score","ratings","reviews","genres","bookFormat","publishedTime","firstPublishedTime",
             "pages","originalTitle","literaryAwards","ISBN","ISBN13","editionLanguage","description","isbnInfo"]
    file = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = file.add_sheet("p_news_goodreads", cell_overwrite_ok=False)
    for i in colum:
        sheet.write(0, colum.index(i), i)

    j=0
    def process_item(self, item, spider):
        j=self.j+1
        self.sheet.write(0, item['cudosid'])
        self.sheet.write(1, item['goodreadsId'])
        self.sheet.write(2, item['goodreadsUrl'])
        self.sheet.write(3, item['title'])
        self.sheet.write(4, item['authorName'])
        self.sheet.write(5, item['authorNameUrl'])
        self.sheet.write(6, item['Illustrator'])
        self.sheet.write(7, item['IllustratorUrl'])
        self.sheet.write(8, item['coverPic'])
        self.sheet.write(9, item['ratingDetails'])
        self.sheet.write(10, item['score'])
        self.sheet.write(11, item['ratings'])
        self.sheet.write(12, item['reviews'])
        self.sheet.write(13, item['genres'])
        self.sheet.write(14, item['bookFormat'])
        self.sheet.write(15, item['publishedTime'])
        self.sheet.write(16, item['firstPublishedTime'])
        self.sheet.write(17, item['pages'])
        self.sheet.write(18, item['originalTitle'])
        self.sheet.write(19, item['literaryAwards'])
        self.sheet.write(20, item['ISBN'])
        self.sheet.write(21, item['ISBN13'])
        self.sheet.write(22, item['editionLanguage'])
        self.sheet.write(23, item['description'])
        self.sheet.write(24, item['isbnInfo'])
        self.file.save('p_news_goodreads.xls')
        return item

    def close_spider(self, spider):
        pass