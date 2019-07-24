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
    name = "goodreads_snapshot"
    custom_settings = {
        'CONCURRENT_REQUESTS': 16,  #允许的线程数
        'RETRY_TIMES': 5,  #重试机制
        # 'DOWNLOAD_DELAY':5,   #延时（秒）
        'ITEM_PIPELINES': {
            "spider_goodreads.pipelines.pipelines_snapshot.SpiderGoodreadsPipeline": 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'spider_goodreads.middlewares.RandomUserAgent.RandomUserAgent': 300,
            # 'spider_goodreads.middlewares.random_http_proxy.IpMiddleware': 110, #添加代理ip逻辑
        },
        # 'LOG_FILE': "goodreads_snapshot.log",
        # 'LOG_LEVEL': "ERROR"
    }

    # start_urls = ['https://www.goodreads.com/book/show/1733202']

    def start_requests(self):
        with open('cudos_goodreads.txt', "r") as f:
            url = f.readlines()
            for x in url:
                datas=x.split("\t")
                cudosId=datas[0]
                goodreadsUrl=datas[1]
                title=datas[2]
                link = goodreadsUrl+"."+"_".join(x for x in title.split(" "))
                goodreadsId=goodreadsUrl.replace("https://www.goodreads.com/book/show/","")
                yield scrapy.Request(link, callback=self.parse,dont_filter=False,meta={"goodreadsId":goodreadsId,"cudosId":cudosId})


    def parse(self, response):
        title = response.xpath("//h1[@id='bookTitle']/text()").extract()[0].strip()
        goodreadsId=re.search("https://www.goodreads.com/book/show/(\d+)",response.url).group(1)
        goodreadsUrl=response.url
        goodreadsAmazonUrl="https://www.goodreads.com"+response.xpath("//ul[@class='buyButtonBar left']/li/a[@class='buttonBar']/@href").extract()[0].strip()

        bookDataBox = response.xpath(XpathRule.bookDataBox).extract()
        infoBoxRowTitle = response.xpath(XpathRule.infoBoxRowTitle).extract()

        if "ISBN" in infoBoxRowTitle:
            ISBN = etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN")]).xpath("./text()")[0].strip()
            ISBN13 = \
            etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN")]).xpath(".//span[@itemprop='isbn']/text()")[
                0].strip() if etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN")]).xpath(
                ".//span[@itemprop='isbn']/text()") else None
        elif "ISBN13" in infoBoxRowTitle:
            ISBN13 = etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN13")]).xpath("./text()")[0].strip()
            ISBN = None
        else:
            ISBN = None
            ISBN13 = None
        amazonUrl="https://www.amazon.com/gp/product/{}".format(ISBN) if ISBN else "https://www.amazon.com/s?k={}".format(
                    "+".join(x for x in re.split(" |,|&|!|\?|:|'",title)))

        storesInfo = response.xpath("//div[@id='buyDropButtonStores']//a[@class='actionLinkLite']")
        for i in storesInfo:
            key = i.xpath("./text()").extract()[0]
            Origin_Url = "https://www.goodreads.com" + str(i.xpath("./@href").extract()[0])
            if "Barnes & Noble" in key:
                goodreadsBarnesNoble = Origin_Url
            if "Walmart eBooks" in key:
                goodreadsWalmarteBooksUrl = Origin_Url
                walmarteBooksUrl = "https://www.kobo.com/us/en/search?query={}".format(
                    "+".join(x for x in title.split(" ")) if len(title.split(":"))==1 else title.split(":")[0])
            if "Alibris" in key:
                goodreadsAlibrisUrl = Origin_Url
            if "Indigo" in key:
                goodreadsIndigo=Origin_Url
            if "IndieBound" in key:
                goodreadsIndieBound=Origin_Url


        yield scrapy.Request(goodreadsBarnesNoble, callback=self.getbarnesNoble,meta={"goodreadsId": goodreadsId,
                                                                              "goodreadsUrl":goodreadsUrl,
                                                                              "title":title,
                                                                              "goodreadsAmazonUrl":goodreadsAmazonUrl,
                                                                              "amazonUrl":amazonUrl,
                                                                              "goodreadsAlibrisUrl":goodreadsAlibrisUrl,
                                                                              "goodreadsWalmarteBooksUrl":goodreadsWalmarteBooksUrl,
                                                                              "goodreadsBarnesNoble":goodreadsBarnesNoble,
                                                                              "walmarteBooksUrl":walmarteBooksUrl,
                                                                              "goodreadsIndigo":goodreadsIndigo,
                                                                              "goodreadsIndieBound":goodreadsIndieBound,
                                                                              "goodreadsId":response.meta["goodreadsId"]})



    def getbarnesNoble(self, response):
        barnesNoble=response.url.split("&")[0]
        yield scrapy.Request(response.meta["goodreadsAlibrisUrl"],
                             callback=self.getalibrisUrl, meta={"goodreadsId": response.meta['goodreadsId'],
                                                                "goodreadsUrl": response.meta['goodreadsUrl'],
                                                                "title": response.meta['title'],
                                                                "goodreadsAmazonUrl": response.meta['goodreadsAmazonUrl'],
                                                                "amazonUrl": response.meta['amazonUrl'],
                                                                "goodreadsAlibrisUrl": response.meta['goodreadsAlibrisUrl'],
                                                                "goodreadsWalmarteBooksUrl": response.meta['goodreadsWalmarteBooksUrl'],
                                                                "goodreadsBarnesNoble": response.meta['goodreadsBarnesNoble'],
                                                                "walmarteBooksUrl": response.meta['walmarteBooksUrl'],
                                                                "goodreadsIndigo": response.meta['goodreadsIndigo'],
                                                                "goodreadsIndieBound": response.meta['goodreadsIndieBound'],
                                                                "barnesNoble":barnesNoble,
                                                                "goodreadsId":response.meta["goodreadsId"]})
    def getalibrisUrl(self,response):
        alibrisUrl=response.url.split("&")[0]
        yield scrapy.Request(response.meta["goodreadsIndigo"],
                             callback=self.getgoodreadsIndigo, meta={"goodreadsId": response.meta['goodreadsId'],
                                                                "goodreadsUrl": response.meta['goodreadsUrl'],
                                                                "title": response.meta['title'],
                                                                "goodreadsAmazonUrl": response.meta[
                                                                    'goodreadsAmazonUrl'],
                                                                "amazonUrl": response.meta['amazonUrl'],
                                                                "goodreadsAlibrisUrl": response.meta[
                                                                    'goodreadsAlibrisUrl'],
                                                                "goodreadsWalmarteBooksUrl": response.meta[
                                                                    'goodreadsWalmarteBooksUrl'],
                                                                "goodreadsBarnesNoble": response.meta[
                                                                    'goodreadsBarnesNoble'],
                                                                "walmarteBooksUrl": response.meta['walmarteBooksUrl'],
                                                                "goodreadsIndigo": response.meta['goodreadsIndigo'],
                                                                "goodreadsIndieBound": response.meta['goodreadsIndieBound'],
                                                                "alibrisUrl":alibrisUrl,
                                                                "barnesNoble": response.meta['barnesNoble'],
                                                                "goodreadsId": response.meta["goodreadsId"]})
    def getgoodreadsIndigo(self,response):
        Indigo=response.url
        yield scrapy.Request(response.meta["goodreadsIndieBound"],
                             callback=self.getgoodreadsIndigo, meta={"goodreadsId": response.meta['goodreadsId'],
                                                                     "goodreadsUrl": response.meta['goodreadsUrl'],
                                                                     "title": response.meta['title'],
                                                                     "goodreadsAmazonUrl": response.meta[
                                                                         'goodreadsAmazonUrl'],
                                                                     "amazonUrl": response.meta['amazonUrl'],
                                                                     "goodreadsAlibrisUrl": response.meta[
                                                                         'goodreadsAlibrisUrl'],
                                                                     "goodreadsWalmarteBooksUrl": response.meta[
                                                                         'goodreadsWalmarteBooksUrl'],
                                                                     "goodreadsBarnesNoble": response.meta[
                                                                         'goodreadsBarnesNoble'],
                                                                     "walmarteBooksUrl": response.meta[
                                                                         'walmarteBooksUrl'],
                                                                     "goodreadsIndigo": response.meta[
                                                                         'goodreadsIndigo'],
                                                                     "goodreadsIndieBound": response.meta[
                                                                         'goodreadsIndieBound'],
                                                                     "Indigo": Indigo,
                                                                     "alibrisUrl":response.meta['alibrisUrl'],
                                                                     "barnesNoble": response.meta['barnesNoble'],
                                                                     "goodreadsId": response.meta["goodreadsId"]})
    def getgoodreadsIndieBound(self,response):
        IndieBound=response.url

        print "\n--------------------图书字段信息-------------------"
        print "   goodreadsId  :"+response.meta['goodreadsId']
        print "   goodreadsUrl    :" + response.meta['goodreadsUrl']
        print "   title    :" + response.meta['title']
        print "   goodreadsAmazonUrl    :" + response.meta['goodreadsAmazonUrl']
        print "   amazonUrl    :" + response.meta['amazonUrl']
        print "   goodreadsAlibrisUrl   :" + response.meta['goodreadsAlibrisUrl']
        print "   alibrisUrl   :" +response.meta['alibrisUrl']
        print "   goodreadsWalmarteBooksUrl    :" + response.meta['goodreadsWalmarteBooksUrl']
        print "   walmarteBooksUrl    :" + response.meta['walmarteBooksUrl']
        print "   goodreadsBarnesNoble    :" + response.meta['goodreadsBarnesNoble']
        print "   barnesNoble    :" + response.meta['barnesNoble']
        print "   goodreadsIndieBound    :" + response.meta['goodreadsIndieBound']
        print "   IndieBound    :" + IndieBound
        print "   goodreadsIndigo    :" + response.meta['goodreadsIndigo']
        print "   Indigo    :" + response.meta['Indigo']
        print "--------------------图书字段信息-------------------\n"
        item = {}
        item["goodreadsId"] = response.meta['goodreadsId']
        item["goodreadsUrl"] = response.meta['goodreadsUrl']
        item["title"] = response.meta['title']
        item["goodreadsAmazonUrl"] = response.meta['goodreadsAmazonUrl']
        item["amazonUrl"] = response.meta['amazonUrl']
        item["goodreadsAlibrisUrl"] = response.meta['goodreadsAlibrisUrl']
        item["alibrisUrl"] = response.meta['alibrisUrl']
        item["goodreadsWalmarteBooksUrl"] = response.meta['goodreadsWalmarteBooksUrl']
        item["walmarteBooksUrl"] = response.meta['walmarteBooksUrl']
        item["goodreadsBarnesNoble"] = response.meta['goodreadsBarnesNoble']
        item["barnesNoble"] = response.meta['barnesNoble']
        item["goodreadsIndieBound"]=response.meta['goodreadsIndieBound']
        item["IndieBound"]=IndieBound
        item["goodreadsIndigo"]=response.meta['goodreadsIndigo']
        item["Indigo"]=response.meta['Indigo']
        print item
