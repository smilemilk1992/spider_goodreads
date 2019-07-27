# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
import re
import requests
import logging
class XpathRule(object):
    bookDataBox = "//div[@class='clearFloats']/div[@class='infoBoxRowItem']"
    details="//div[@id='details']/div[@class='row']"
    infoBoxRowTitle="//div[@class='clearFloats']/div[@class='infoBoxRowTitle']/text()"


class GoodReadsSpider(scrapy.Spider):
    '''
    图书信息
    '''
    name = "goodreads1"
    custom_settings = {
        'CONCURRENT_REQUESTS': 8,  #允许的线程数
        'RETRY_TIMES': 3,  #重试机制
        # 'DOWNLOAD_DELAY':5,   #延时（秒）
        'ITEM_PIPELINES': {
            # "spider_goodreads.pipelines.pipelines.SpiderGoodreadsPipeline": 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'spider_goodreads.middlewares.RandomUserAgent.RandomUserAgent': 300,
            # 'spider_goodreads.middlewares.random_http_proxy.IpMiddleware': 110, #添加代理ip逻辑
        },
        # 'LOG_FILE': "goodreads.log",
        # 'LOG_LEVEL': "ERROR"
    }

    # start_urls = ['https://www.goodreads.com/book/show/1733202']

    def start_requests(self):
        with open('cudos_goodreads.txt', "r") as f:
            url = f.readlines()
            for x in url:
                datas=x.strip().split("\t")
                cudosid = int(datas[0])
                goodreadsid = int(datas[1].replace("https://www.goodreads.com/book/show/", ""))
                goodreadsUrl = datas[1]
                goodreadsReq=datas[1]+"."+"_".join(i for i in datas[2].split(" "))
                title = datas[2]
                author = datas[3]
                yield scrapy.Request(goodreadsReq, callback=self.parse,
                                     dont_filter=False,
                                     meta={"goodreadsid":goodreadsid,
                                           "cudosid":cudosid,
                                           "title":title,
                                           "flag":False,
                                           "isbninfo":{}})


    def parse(self, response):
        reqId = re.search("book/show/(\d+)",response.url).group(1)
        bookDataBox = response.xpath(XpathRule.bookDataBox).extract()
        infoBoxRowTitle = response.xpath(XpathRule.infoBoxRowTitle).extract()
        if "ISBN" in infoBoxRowTitle:
            ISBN = etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN")]).xpath("./text()")[0].strip()
            ISBN13 = \
            etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN")]).xpath(".//span[@itemprop='isbn']/text()")[
                0].strip() if etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN")]).xpath(
                ".//span[@itemprop='isbn']/text()") else "None"
        elif "ISBN13" in infoBoxRowTitle:
            ISBN13 = etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN13")]).xpath("./text()")[0].strip()
            ISBN = "None"
        else:
            ISBN = "None"
            ISBN13 = "None"
        isbninfo=response.meta["isbninfo"]
        isbninfo[reqId]=[ISBN,ISBN13]
        if reqId is response.meta["goodreadsid"]:
            flag=True
            otherEdition=response.xpath("//div[@class='otherEdition']/a/@href").extract()
            otherEditionUrl ={}
            if otherEdition:
                for o in otherEdition:
                    id=re.search("book/show/(\d+)",o).group(1)
                    otherEditionUrl[id]=o
                    yield scrapy.Request(o, callback=self.parse, dont_filter=False, meta={"goodreadsid": response.meta["goodreadsid"],
                                                                                             "cudosid":response.meta["cudosid"],
                                                                                             "title":response.meta["title"],
                                                                                          "flag":flag,
                                                                                          "isbninfo":isbninfo})


        if response.meta['flag']:
            print response.meta["goodreadsid"],isbninfo



