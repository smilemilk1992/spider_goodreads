# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
class XpathRule(object):
    bookDataBox = "//div[@id='bookDataBox']/div[@class='clearFloats']"



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
    start_urls = ['https://www.goodreads.com/book/show/1733202']

    def parse(self, response):

        title=response.xpath("//h1[@id='bookTitle']/text()").extract()[0].strip()
        authorNameUrl=response.xpath("//a[@class='authorName']/@href").extract()[0].strip()
        authorName = response.xpath("//a[@class='authorName']/span/text()").extract()[0].strip()
        score=response.xpath("//span[@itemprop='ratingValue']/text()").extract()[0].strip()
        ratings=response.xpath("//meta[@itemprop='ratingCount']/@content").extract()[0].strip()
        reviews = response.xpath("//meta[@itemprop='reviewCount']/@content").extract()[0].strip()
        description=response.xpath("//div[@id='description']/span/text()").extract()[0].strip()
        bookFormat=response.xpath("//span[@itemprop='bookFormat']/text()").extract()[0].strip()
        bookDataBox=response.xpath(XpathRule.bookDataBox).extract()
        list=[]
        for i in bookDataBox:
            i = etree.fromstring(i)
            data = i.xpath("/div[@class='infoBoxRowItem']/text()").extract()[0].strip()
            list.append(data)


        print "   title    :"+title
        print "   authorName    :"+authorName
        print "   authorNameUrl    :"+authorNameUrl
        print "   score    :" + score
        print "   ratings    :" + ratings
        print "   reviews    :" + reviews
        print "   bookFormat    :" + bookFormat
        print "   Original_itle    :" + list
        print "   description    :" + description




