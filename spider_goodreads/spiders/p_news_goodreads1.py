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
                                           "title":title})


    def parse(self, response):
        actionLinkLite="https://www.goodreads.com"+response.xpath("//div[@class='otherEditionsActions']/a[@class='actionLinkLite']/@href").extract()[0]
        yield scrapy.Request(actionLinkLite+"?per_page=100", callback=self.otherLink,dont_filter=False,meta={"goodreadsid":response.meta["goodreadsid"]})

    def otherLink(self,response):
        xx=[]
        moreDetails=response.xpath("//div[@class='moreDetails hideDetails']").extract()
        for i in moreDetails:
            i=etree.fromstring(i)
            dataRow=i.xpath("./div[@class='dataRow']")
            for data in dataRow:
                dataTitle=data.xpath("./div[@class='dataTitle']/text()")[0].strip()
                if "ISBN" in dataTitle:
                    ISBN=data.xpath("./div[@class='dataValue']/text()")[0].strip()
                    ISBN13=data.xpath("./div[@class='dataValue']/span[@class='greyText']/text()")[0].strip() if data.xpath("./div[@class='dataValue']/span[@class='greyText']/text()") else None
                    xx.append([ISBN,ISBN13.lstrip("(ISBN13: ").rstrip(")")])
                elif "ISBN13" in dataTitle:
                    ISBN13 = data.xpath(".//div[@class='dataValue']/text()")[0].strip()
                    ISBN=None
                    xx.append([ISBN, ISBN13.lstrip("(ISBN13: ").rstrip(")")])
        print response.meta["goodreadsid"],xx












