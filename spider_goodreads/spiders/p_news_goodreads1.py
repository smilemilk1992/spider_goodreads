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
            "//div[@id='description']//p//text()|//div[@id='description']/span//text()").extract()) if response.xpath(
            "//div[@id='description']//p//text()|//div[@id='description']/span//text()").extract() else "None"
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
            a = etree.fromstring(details[0]).xpath("./text()")[0] if etree.fromstring(details[0]).xpath(
                "./text()") else None
            aa = "".join(x.strip() + " " for x in a.split("\n") if x)
            bb = etree.fromstring(details[0]).xpath("./nobr[@class='greyText']/text()")[0].strip().rstrip(
                ")").lstrip("(") if etree.fromstring(details[0]).xpath("./nobr[@class='greyText']/text()") else aa
        else:
            aa = None
            bb = None
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

            if a:
                genres[a] = b.replace("users", "").strip() if b else None
            else:
                genres = "None"
        item = {}
        item["cudosid"]=response.meta["cudosid"]
        item["goodreadsId"] = re.search("https://www.goodreads.com/book/show/(\d+)", response.url).group(1)
        item["goodreadsUrl"] = response.url
        item["title"] = title
        item["authorName"] = ",".join(x for x in authorList)
        item["authorNameUrl"] = ",".join(x for x in authorUrlList)
        item["Illustrator"] = ",".join(x for x in Tlluser)
        item["IllustratorUrl"] = ",".join(x for x in Tllist)
        item["coverPic"] = coverPic
        item["ratingDetails"] = renderRatingGraph
        item["score"] = score
        item["ratings"] = ratings
        item["reviews"] = reviews
        item["ISBN"] = ISBN
        item["ISBN13"] = ISBN13.lstrip("(ISBN13: ").rstrip(")") if ISBN13 else None
        item["genres"] = str(genres).replace("'", "\'") if genres else None
        item["bookFormat"] = bookFormat.replace("'", "\'")
        item["publishedTime"] = aa.replace("'", "\'")
        item["firstPublishedTime"] = bb.replace("'", "\'")
        item["pages"] = pages
        item["originalTitle"] = Original_title.replace("'", "\'")
        item["literaryAwards"] = Literary_Awards.replace("'", "\'")
        item["editionLanguage"] = Edition_Language.replace("'", "\'")
        item['description'] = description.replace("'", "\'")

        otherEditionsActions=response.xpath("//div[@class='otherEditionsActions']/a[@class='actionLinkLite']/@href").extract()
        if otherEditionsActions:
            actionLinkLite="https://www.goodreads.com"+otherEditionsActions[0]
            yield scrapy.Request(actionLinkLite+"?per_page=100", callback=self.otherLink,dont_filter=False,meta={"goodreadsid":response.meta["goodreadsid"],"item":item})
        else:
            isbninfo = {}
            isbninfo[response.meta["goodreadsid"]]=[ISBN,ISBN13]
            item["isbninfo"]=isbninfo
            print "-----------",response.meta["goodreadsid"]



    def otherLink(self,response):
        isbninfo={}
        infolist = response.xpath("//div[@class='editionData']").extract()
        for info in infolist:
            info =etree.fromstring(info)
            infoUrl=info.xpath(".//a[@class='bookTitle']/@href")[0].strip()
            infoId=re.search("book/show/(\d+)",infoUrl).group(1)
            if infoId is response.meta["goodreadsid"]:
                continue
            moreDetails=info.xpath(".//div[@class='moreDetails hideDetails']")

            for i in moreDetails:
                dataRow=i.xpath("./div[@class='dataRow']")
                for data in dataRow:
                    isbninfo[infoId] = [None, None]
                    dataTitle=data.xpath("./div[@class='dataTitle']/text()")[0].strip()
                    print "----",dataTitle
                    if "ISBN13" in dataTitle:
                        ISBN13 = data.xpath(".//div[@class='dataValue']/text()")[0].strip()
                        ISBN=None
                        isbninfo[infoId]=[ISBN, ISBN13.lstrip("(ISBN13: ").rstrip(")")]

                    elif "ISBN" in dataTitle:
                        ISBN=data.xpath("./div[@class='dataValue']/text()")[0].strip()
                        ISBN13=data.xpath("./div[@class='dataValue']/span[@class='greyText']/text()")[0].strip() if data.xpath("./div[@class='dataValue']/span[@class='greyText']/text()") else None
                        isbninfo[infoId]=[ISBN,ISBN13.lstrip("(ISBN13: ").rstrip(")") if ISBN13 else None]

        item=response.meta["item"]
        print "\n--------------------图书字段信息-------------------"
        print "   cudosid  :" + str(item["cudosid"])
        print "   goodreadsId  :" + str(item["goodreadsId"])
        print "   goodreadsUrl    :" + item["goodreadsUrl"]
        print "   title    :" + item["title"]
        print "   authorName    :" + item["authorName"]
        print "   authorNameUrl    :" + item["authorNameUrl"]
        print "   Illustrator   :" + item["Illustrator"]
        print "   IllustratorUrl   :" + item["IllustratorUrl"]
        print "   coverPic    :" + item["coverPic"]
        print "   ratingDetails    :" + item["ratingDetails"]
        print "   score    :" + item["score"]
        print "   ratings    :" + item["ratings"]
        print "   reviews    :" + item["reviews"]
        print "   genres     :" + item["genres"]
        print "   bookFormat    :" + item["bookFormat"]
        print "   publishedTime    :" + item["publishedTime"]
        print "   firstPublishedTime    :" + item["firstPublishedTime"]
        print "   pages    :" + item["pages"]
        print "   ISBN    :" + item["ISBN"]
        print "   ISBN13    :" + item["ISBN13"]
        print "   originalTitle    :" + item["originalTitle"]
        print "   literaryAwards   :" + item["literaryAwards"]
        print "   editionLanguage    :" + item["editionLanguage"]
        print "   description    :" + item["description"]
        print "   isbnInfo    :" + str(isbninfo)
        print "--------------------图书字段信息-------------------\n"













