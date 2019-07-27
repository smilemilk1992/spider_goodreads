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
        'CONCURRENT_REQUESTS': 16,  #允许的线程数
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
                yield scrapy.Request(goodreadsReq, callback=self.parse,dont_filter=False,meta={"goodreadsid":goodreadsid})


    def parse(self, response):
        otherEdition=response.xpath("//div[@class='otherEdition']/a/@href").extract()
        otherEditionUrl ={}
        if otherEdition:
            for o in otherEdition:
                id=re.search("book/show/(\d+)",o).group(1)
                otherEditionUrl[id]=o
        print requests.url,otherEditionUrl
