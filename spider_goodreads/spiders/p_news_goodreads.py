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
    name = "goodreads"
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
        }
    }

    start_urls = ['https://www.goodreads.com/book/show/2476280']

    # def start_requests(self):
    #     with open('url.txt', "r") as f:
    #         url = f.readlines()
    #         for x in url:
    #             yield scrapy.Request(x.strip(), callback=self.parse)


    def parse(self, response):
        score = response.xpath("//span[@itemprop='ratingValue']/text()").extract()[0].strip()
        reviews = response.xpath("//meta[@itemprop='reviewCount']/@content").extract()[0].strip()
        ratings = response.xpath("//meta[@itemprop='ratingCount']/@content").extract()[0].strip()
        bookUrl = response.url
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

        coverPic = \
        response.xpath("//div[@class='noCoverMediumContainer']/img/@src | //img[@id='coverImage']/@src").extract()[
            0].strip()
        description = ",".join(x.strip() for x in response.xpath(
            "//div[@id='description']//p//text()|//div[@id='description']/span/text()").extract()) if response.xpath(
            "//div[@id='description']//p//text()|//div[@id='description']/span/text()").extract() else "None"
        bookFormat = response.xpath("//span[@itemprop='bookFormat']/text()").extract()[0].strip() if response.xpath(
            "//span[@itemprop='bookFormat']/text()").extract() else "None"
        ispage = response.xpath("//span[@itemprop='numberOfPages']/text()").extract()
        if ispage:
            pages = response.xpath("//span[@itemprop='numberOfPages']/text()").extract()[0].strip().replace(" pages",
                                                                                                            "")
        else:
            pages = "None"

        bookDataBox = response.xpath(XpathRule.bookDataBox).extract()
        infoBoxRowTitle = response.xpath(XpathRule.infoBoxRowTitle).extract()
        if "Original Title" in infoBoxRowTitle:
            Original_title = etree.fromstring(bookDataBox[infoBoxRowTitle.index("Original Title")]).xpath("./text()")[
                0].strip()
        else:
            Original_title = "None"

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
        if "Edition Language" in infoBoxRowTitle:
            Edition_Language = \
            etree.fromstring(bookDataBox[infoBoxRowTitle.index("Edition Language")]).xpath("./text()")[
                0].strip() if etree.fromstring(bookDataBox[infoBoxRowTitle.index("Edition Language")]).xpath(
                "./text()") else "None"
        else:
            Edition_Language = "None"

        if "Literary Awards" in infoBoxRowTitle:
            Literary_Awards = ",".join(x for x in
                                       etree.fromstring(bookDataBox[infoBoxRowTitle.index("Literary Awards")]).xpath(
                                           "./a[@class='award']/text()"))
        else:
            Literary_Awards = "None"

        details = response.xpath(XpathRule.details).extract()
        if len(details) >= 2:
            a = etree.fromstring(details[1]).xpath("./text()")[0]
            aa = "".join(x.strip() + " " for x in a.split("\n") if x)
            bb = etree.fromstring(details[1]).xpath("./nobr[@class='greyText']/text()")[0].strip().rstrip(")").lstrip(
                "(") if etree.fromstring(details[1]).xpath("./nobr[@class='greyText']/text()") else aa
        elif len(details) == 1:
            a = etree.fromstring(details[0]).xpath("./text()")[0] if etree.fromstring(details[0]).xpath("./text()") else "None"
            aa = "".join(x.strip() + " " for x in a.split("\n") if x)
            bb = etree.fromstring(details[0]).xpath("./nobr[@class='greyText']/text()")[0].strip().rstrip(
                ")").lstrip("(") if etree.fromstring(details[0]).xpath("./nobr[@class='greyText']/text()") else aa
        else:
            aa = "None"
            bb = "None"
        Rating_details = response.xpath(
            "//span[@id='rating_graph']/script/text()|//span[@id='reviewControls__ratingDetailsMiniGraph']/script/text()").extract()[
            0].strip()

        renderRatingGraph = re.search("\[(.*?)\]", Rating_details).group(1)

        elementList = response.xpath(
            "//div[@class='bigBoxContent containerWithHeaderContent']/div[contains(@class,'elementList ')]").extract()

        genres = {}
        for x in elementList:
            x = etree.fromstring(x)
            actionLinkLite = x.xpath(".//a[@class='actionLinkLite bookPageGenreLink']/text()")
            if len(actionLinkLite) == 2:
                a = ">".join(x.strip() for x in actionLinkLite)
            else:
                if actionLinkLite:
                    a = actionLinkLite[0].strip()
                else:
                    a = None

            bookPageGenreLink = x.xpath(".//a[@class='actionLinkLite greyText bookPageGenreLink']/text()")
            if bookPageGenreLink:
                b = bookPageGenreLink[0].strip()
            else:
                b = None

            if a :
                genres[a] = b.replace("users", "").strip() if b else None
            else:
                genres = "None"





        print "\n--------------------图书字段信息-------------------"
        print "   bookUrl    :" + bookUrl
        print "   title    :" + title
        print "   authorName    :" + ",".join(x for x in authorList)
        print "   authorNameUrl    :" + ",".join(x for x in authorUrlList)
        print "   Illustrator   :" + ",".join(x for x in Tlluser)
        print "   IllustratorUrl   :" + ",".join(x for x in Tllist)
        print "   coverPic    :" + coverPic
        print "   Rating details    :" + renderRatingGraph
        print "   score    :" + score
        print "   ratings    :" + ratings
        print "   reviews    :" + reviews
        print "   genres     :" + str(genres if genres else "None")
        print "   bookFormat    :" + bookFormat
        print "   Published_Time    :" + aa
        print "   First_Published_Time    :" + bb
        print "   pages    :" + pages
        print "   Original_title    :" + Original_title
        print "   Literary_Awards   :" + Literary_Awards
        print "   ISBN    :" + ISBN
        print "   ISBN13    :" + ISBN13
        print "   Edition_Language    :" + Edition_Language
        print "   description    :" + description
        print "--------------------图书字段信息-------------------\n"
