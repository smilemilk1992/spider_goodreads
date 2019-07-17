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
        # 'LOG_FILE': "goodreads_snapshot.log",
        # 'LOG_LEVEL': "ERROR"
    }

    start_urls = ['https://www.goodreads.com/book/show/488924']

    # def start_requests(self):
    #     with open('url.txt', "r") as f:
    #         url = f.readlines()
    #         for x in url:
    #             id=re.search("https://www.goodreads.com/book/show/(\d+)",x.strip()).group(1)
    #             yield scrapy.Request(x.strip(), callback=self.parse,dont_filter=False)


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
                    "+".join(x for x in title.split(" ")))

        storesInfo = response.xpath("//div[@id='buyDropButtonStores']//a[@class='actionLinkLite']")
        for i in storesInfo:
            key = i.xpath("./text()").extract()[0]
            Origin_Url = "https://www.goodreads.com" + str(i.xpath("./@href").extract()[0])
            if "Barnes & Noble" in key:
                goodreadsBarnesNoble = Origin_Url
                # barnesNoble = requests.get(Origin_Url, allow_redirects=True).url
            if "Walmart eBooks" in key:
                goodreadsWalmarteBooksUrl = Origin_Url
                walmarteBooksUrl = "https://www.kobo.com/us/en/search?query={}".format(
                    "+".join(x for x in title.split(" ")))

            if "Alibris" in key:
                goodreadsAlibrisUrl = Origin_Url
                alibrisUrl="https://www.alibris.com/booksearch?keyword={}".format(ISBN) if ISBN else re.search('isbn: (\d+)',response.body).group(1)

        yield scrapy.Request(goodreadsBarnesNoble, callback=self.parse1, meta={"goodreadsId": goodreadsId,
                                                                                                  "goodreadsUrl":goodreadsUrl,
                                                                                                  "title":title,
                                                                                                  "goodreadsAmazonUrl":goodreadsAmazonUrl,
                                                                                                  "amazonUrl":amazonUrl,
                                                                                                  "goodreadsAlibrisUrl":goodreadsAlibrisUrl,
                                                                                                  "goodreadsWalmarteBooksUrl":goodreadsWalmarteBooksUrl,
                                                                                                  "goodreadsBarnesNoble":goodreadsBarnesNoble,
                                                                               "walmarteBooksUrl":walmarteBooksUrl,
                                                                               "alibrisUrl":alibrisUrl})



    def parse1(self, response):
        barnesNoble=response.url.split("?ean=")[0]

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
        print "   barnesNoble    :" + barnesNoble

        print "--------------------图书字段信息-------------------\n"
        # item = {}
        # item["goodreadsId"] = re.search("https://www.goodreads.com/book/show/(\d+)",response.url).group(1)
        # item["relationId"] = response.meta["id"]
        # item["goodreadsUrl"] = response.url
        # item["title"] = title
        # item["authorName"] = ",".join(x for x in authorList)
        # item["authorNameUrl"] = ",".join(x for x in authorUrlList)
        # item["Illustrator"] = ",".join(x for x in Tlluser)
        # item["IllustratorUrl"] = ",".join(x for x in Tllist)
        # item["coverPic"] = coverPic
        # item["ratingDetails"] = renderRatingGraph
        # item["score"] = score
        # item["ratings"] = ratings
        # item["reviews"] = reviews
        # item["genres"] = str(genres).replace("'","\'") if genres else None
        # item["bookFormat"] = bookFormat.replace("'","\'")
        # item["publishedTime"]=aa.replace("'","\'")
        # item["firstPublishedTime"] = bb.replace("'","\'")
        # item["pages"] = pages
        # item["originalTitle"] = Original_title.replace("'","\'")
        # item["literaryAwards"] = Literary_Awards.replace("'","\'")
        # item["ISBN"] = ISBN
        # item["ISBN13"] = ISBN13
        # item["editionLanguage"] = Edition_Language.replace("'","\'")
        # item['description']=description.replace("'","\'")
        # yield item
