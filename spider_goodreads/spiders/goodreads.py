# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
import re
class XpathRule(object):
    bookDataBox = "//div[@class='clearFloats']/div[@class='infoBoxRowItem']"
    details="//div[@id='details']/div[@class='row']"


class MangoSpider(scrapy.Spider):
    name = "goodreads"
    custom_settings = {
        'CONCURRENT_REQUESTS': 64,  #允许的线程数
        'RETRY_TIMES': 3,  #重试机制
        'DOWNLOAD_DELAY':0.5,   #延时（秒）
        # 'ITEM_PIPELINES': {
        #     "spider_goodreads.pipelines.SpiderPipeline": 200,
        # },
        'DOWNLOADER_MIDDLEWARES': {
            'spider_goodreads.middlewares.RandomUserAgent.RandomUserAgent': 300,
            # 'spider_goodreads.middlewares.random_http_proxy.IpMiddleware': 110, #添加代理ip逻辑
        }
    }

# https://www.goodreads.com/author/list/93621.Ellen_Jackson   作者书籍清单
    #开始种子URL
    start_urls = ['https://www.goodreads.com/book/show/38256483']

    def parse(self, response):

        title=response.xpath("//h1[@id='bookTitle']/text()").extract()[0].strip()
        authorNameUrl=",".join(x.strip() for x in response.xpath("//a[@class='authorName']/@href").extract())
        authorName = ",".join(x.strip() for x in response.xpath("//a[@class='authorName']/span/text()").extract())
        score=response.xpath("//span[@itemprop='ratingValue']/text()").extract()[0].strip()
        print "------"+score
        ratings=response.xpath("//meta[@itemprop='ratingCount']/@content").extract()[0].strip()
        reviews = response.xpath("//meta[@itemprop='reviewCount']/@content").extract()[0].strip()
        coverPic=response.xpath("//div[@class='noCoverMediumContainer']/img/@src | //img[@id='coverImage']/@src").extract()[0].strip()
        description=response.xpath("//div[@id='description']/span/text()").extract()[0].strip() if response.xpath("//div[@id='description']/span/text()").extract() else "None"
        bookFormat=response.xpath("//span[@itemprop='bookFormat']/text()").extract()[0].strip()
        ispage=response.xpath("//span[@itemprop='numberOfPages']/text()").extract()
        if ispage:
            pages=response.xpath("//span[@itemprop='numberOfPages']/text()").extract()[0].strip().replace(" pages","")
        else:
            pages="None"
        bookDataBox=response.xpath(XpathRule.bookDataBox).extract()
        if etree.fromstring(bookDataBox[0]).xpath("./text()"):
            Original_itle=etree.fromstring(bookDataBox[0]).xpath("./text()")[0].strip()
            ISBN=etree.fromstring(bookDataBox[1]).xpath("./text()")[0].strip()
            ISBN13 = etree.fromstring(bookDataBox[1]).xpath(".//span[@itemprop='isbn']/text()")[0].strip()
            Edition_Language=etree.fromstring(bookDataBox[2]).xpath("./text()")[0].strip()
        else:
            Original_itle = "None"
            ISBN = etree.fromstring(bookDataBox[0]).xpath("./text()")[0].strip()
            ISBN13 = etree.fromstring(bookDataBox[0]).xpath(".//span[@itemprop='isbn']/text()")[0].strip()
            Edition_Language = etree.fromstring(bookDataBox[1]).xpath("./text()")[0].strip()

        details=response.xpath(XpathRule.details).extract()
        a=etree.fromstring(details[1]).xpath("./text()")[0]
        aa="".join(x.strip()+" " for x in a.split("\n") if x)
        bb=etree.fromstring(details[1]).xpath("./nobr[@class='greyText']/text()")[0].strip().rstrip(")").lstrip("(") if etree.fromstring(details[1]).xpath("./nobr[@class='greyText']/text()") else aa

        Rating_details=response.xpath("//span[@id='rating_graph']/script/text()").extract()[0].strip()
        renderRatingGraph=re.search("renderRatingGraph\(\[(.*?)\]\);",Rating_details).group(1)

        print "\n--------------------图书字段信息-------------------"
        print "   title    :"+title
        print "   authorName    :"+authorName
        print "   authorNameUrl    :"+authorNameUrl
        print "   coverPic    :" + coverPic
        print "   Rating details    :" + renderRatingGraph
        print "   score    :" + score
        print "   ratings    :" + ratings
        print "   reviews    :" + reviews
        print "   bookFormat    :" + bookFormat
        print "   Published_Time    :" + aa
        print "   First_Published_Time    :" + bb
        print "   pages    :" + pages
        print "   Original_itle    :" + Original_itle
        print "   ISBN    :" + ISBN
        print "   ISBN13    :" + ISBN13
        print "   Edition_Language    :" + Edition_Language
        print "   description    :" + description

        print "--------------------图书字段信息-------------------\n"




