# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
class XpathRule(object):
    bookDataBox = "//div[@class='clearFloats']/div[@class='infoBoxRowItem']"



class MangoSpider(scrapy.Spider):
    name = "goodreads"
    custom_settings = {
        'CONCURRENT_REQUESTS': 64,  #允许的线程数
        'RETRY_TIMES': 3,  #重试机制
        # 'DOWNLOAD_DELAY':0.5,   #延时（秒）
        # 'ITEM_PIPELINES': {
        #     "spider_goodreads.pipelines.SpiderPipeline": 200,
        # },
        'DOWNLOADER_MIDDLEWARES': {
            'spider_goodreads.middlewares.RandomUserAgent.RandomUserAgent': 300,
            # 'spider_goodreads.middlewares.random_http_proxy.IpMiddleware': 110, #添加代理ip逻辑
        }
    }

    #开始种子URL
    start_urls = ['https://www.goodreads.com/book/show/15159113']

    def parse(self, response):

        title=response.xpath("//h1[@id='bookTitle']/text()").extract()[0].strip()
        authorNameUrl=response.xpath("//a[@class='authorName']/@href").extract()[0].strip()
        authorName = response.xpath("//a[@class='authorName']/span/text()").extract()[0].strip()
        score=response.xpath("//span[@itemprop='ratingValue']/text()").extract()[0].strip()
        ratings=response.xpath("//meta[@itemprop='ratingCount']/@content").extract()[0].strip()
        reviews = response.xpath("//meta[@itemprop='reviewCount']/@content").extract()[0].strip()
        coverPic=response.xpath("//div[@class='noCoverMediumContainer']/img/@src | //img[@id='coverImage']/@src").extract()[0].strip()
        description=response.xpath("//div[@id='description']/span/text()").extract()[0].strip()
        bookFormat=response.xpath("//span[@itemprop='bookFormat']/text()").extract()[0].strip()
        ispage=response.xpath("//span[@itemprop='numberOfPages']/text()").extract()
        if ispage:
            pages=response.xpath("//span[@itemprop='numberOfPages']/text()").extract()[0].strip().replace(" pages","")
        else:
            pages="None"
        bookDataBox=response.xpath(XpathRule.bookDataBox).extract()
        Original_itle=etree.fromstring(bookDataBox[0]).xpath("./text()")[0].strip()
        ISBN=etree.fromstring(bookDataBox[1]).xpath("./text()")[0].strip()
        ISBN13 = etree.fromstring(bookDataBox[1]).xpath(".//span[@itemprop='isbn']/text()")[0].strip()
        Edition_Language=etree.fromstring(bookDataBox[2]).xpath("./text()")[0].strip()
        print "--------------------图书字段信息-------------------\n"
        print "   title    :"+title
        print "   authorName    :"+authorName
        print "   authorNameUrl    :"+authorNameUrl
        print "   coverPic    :" + coverPic
        print "   score    :" + score
        print "   ratings    :" + ratings
        print "   reviews    :" + reviews
        print "   bookFormat    :" + bookFormat
        print "   pages    :" + pages
        print "   Original_itle    :" + Original_itle
        print "   ISBN    :" + ISBN
        print "   ISBN13    :" + ISBN13
        print "   Edition_Language    :" + Edition_Language
        print "   description    :" + description

        print "--------------------图书字段信息-------------------\n"




