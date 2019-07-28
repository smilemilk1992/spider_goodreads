# -*- coding: utf-8 -*-
import traceback
import MySQLdb
import xlwt
from openpyxl import Workbook


class SpiderGoodreadsPipelineCSV(object):
    '''
    保存到excel
    '''

    def __init__(self):
        colum = ["cudosid", "goodreadsId", "goodreadsUrl", "title", "authorName", "authorNameUrl", "Illustrator",
                 "IllustratorUrl",
                 "coverPic", "ratingDetails", "score", "ratings", "reviews", "genres", "bookFormat", "publishedTime",
                 "firstPublishedTime",
                 "pages", "originalTitle", "literaryAwards", "ISBN", "ISBN13", "editionLanguage", "description",
                 "isbnInfo"]
        self.wb = Workbook()  # 类实例化
        self.ws = self.wb.active  # 激活工作表
        self.ws.append(colum)  # 添加表头


    def process_item(self, item, spider):
        data = [item['cudosid'],item['goodreadsId'],item['goodreadsUrl'],item['title'],item['authorName'],item['authorNameUrl'],
                item['Illustrator'],item['IllustratorUrl'],item['coverPic'],item['ratingDetails'],item['score'],item['ratings'],
                item['reviews'],item['genres'],item['bookFormat'],item['publishedTime'],item['firstPublishedTime'],item['pages'],
                item['originalTitle'],item['literaryAwards'],item['ISBN'],item['ISBN13'],item['editionLanguage'],item['description'],item['isbnInfo']]
        self.ws.append(data)  # 将数据以行的形式添加到工作表中
        self.wb.save('p_news_goodreads.xlsx')  # 保存
        return item

    def close_spider(self, spider):
        pass