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
    name = "goodreads_library"
    custom_settings = {
        'CONCURRENT_REQUESTS': 48,  #允许的线程数
        'RETRY_TIMES': 3,  #重试机制
        # 'DOWNLOAD_DELAY':5,   #延时（秒）
        'ITEM_PIPELINES': {
            "spider_goodreads.pipelines.pipelines.SpiderGoodreadsPipeline": 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'spider_goodreads.middlewares.RandomUserAgent.RandomUserAgent': 300,
            # 'spider_goodreads.middlewares.random_http_proxy.IpMiddleware': 110, #添加代理ip逻辑
        },
        'LOG_FILE': "goodreads.log",
        'LOG_LEVEL': "ERROR"
    }

    # start_urls = ['https://www.goodreads.com/book/show/1733202']

    def start_requests(self):
        with open('url.txt', "r") as f:
            url = f.readlines()
            for x in url:
                id=re.search("https://www.goodreads.com/book/show/(\d+)",x.strip()).group(1)
                yield scrapy.Request(x.strip(), callback=self.parse,dont_filter=False,meta={"id":id})


    def parse(self, response):

        title = response.xpath("//h1[@id='bookTitle']/text()").extract()[0].strip()
        Tllist = []
        Tlluser = []
        authorUrlList = []
        authorList = []
        for x in response.xpath("//div[@class='authorName__container']").extract():
            x = etree.fromstring(x)
            greyText = x.xpath(".//span[contains(@class,'greyText')]/text()")
            if greyText:
                if "Illustrator" in x.xpath("./span[contains(@class,'greyText')]/text()")[0].strip():
                    Tllist.append(x.xpath("./a[@class='authorName']/@href")[0].strip())
                    Tlluser.append(x.xpath("./a[@class='authorName']/span/text()")[0].strip())
                else:
                    authorUrlList.append(x.xpath("./a[@class='authorName']/@href")[0].strip())
                    authorList.append(x.xpath("./a[@class='authorName']/span/text()")[0].strip())
            else:
                authorUrlList.append(x.xpath("./a[@class='authorName']/@href")[0].strip())
                authorList.append(x.xpath("./a[@class='authorName']/span/text()")[0].strip())
        authorName=",".join(x for x in authorList)
        Illustrator=",".join(x for x in Tlluser)
        libraryUrl = "https://www.goodreads.com"+response.xpath("//a[@rel='nofollow noopener noreferrer']/@href").extract()[-1].strip()
        yield scrapy.Request(libraryUrl, callback=self.worldUrl, meta={"title": title,"authorName":authorName,"Illustrator":Illustrator})


    def worldUrl(self,response):
        worldcatUrl=response.url






