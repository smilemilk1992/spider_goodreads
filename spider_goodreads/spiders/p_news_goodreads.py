# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class XpathRule(object):
    score="//span[@itemprop='ratingValue']/text()"
    reviews="//meta[@itemprop='reviewCount']/@content"
    ratings="//meta[@itemprop='ratingCount']/@content"
    title="//h1[@id='bookTitle']/text()"
    authorName__container="//div[@class='authorName__container']"
    cover="//div[@class='noCoverMediumContainer']/img/@src | //img[@id='coverImage']/@src"
    description="//div[@id='description']//p//text()|//div[@id='description']/span//text()"
    bookFormat="//span[@itemprop='bookFormat']/text()"
    bookDataBox = "//div[@class='clearFloats']/div[@class='infoBoxRowItem']"
    numberOfPages="//span[@itemprop='numberOfPages']/text()"
    isbn=".//span[@itemprop='isbn']/text()"
    details="//div[@id='details']/div[@class='row']"
    greyText="./nobr[@class='greyText']/text()"
    elementList="//div[@class='bigBoxContent containerWithHeaderContent']/div[contains(@class,'elementList ')]"
    Rating_details="//span[@id='rating_graph']/script/text()|//span[@id='reviewControls__ratingDetailsMiniGraph']/script/text()"
    infoBoxRowTitle="//div[@class='clearFloats']/div[@class='infoBoxRowTitle']/text()"


class GoodReadsSpider(scrapy.Spider):
    '''
    图书信息
    '''
    name = "goodreads"
    custom_settings = {
        'CONCURRENT_REQUESTS': 8,  #允许的线程数
        'RETRY_TIMES': 3,  #重试机制
        # 'DOWNLOAD_DELAY':5,   #延时（秒）
        'ITEM_PIPELINES': {
            # "spider_goodreads.pipelines.pipelines.SpiderGoodreadsPipeline": 200, #入mysql
            "spider_goodreads.pipelines.pipelines_csv.SpiderGoodreadsPipelineCSV": 200, #入csv
        },
        'DOWNLOADER_MIDDLEWARES': {
            'spider_goodreads.middlewares.RandomUserAgent.RandomUserAgent': 300,
            # 'spider_goodreads.middlewares.random_http_proxy.IpMiddleware': 110, #添加代理ip逻辑
        },
    }

    # start_urls = ['https://www.goodreads.com/book/show/1733202']

    def start_requests(self):
        with open('cudos_goodreads.txt', "r") as f:
            url = f.readlines()
            for x in url:
                datas=x.strip().split("\t")
                cudosid = int(datas[0])
                goodreadsid = int(datas[1].replace("https://www.goodreads.com/book/show/", ""))
                goodreadsReq=datas[1]+"."+"_".join(i for i in datas[2].split(" "))
                yield scrapy.Request(goodreadsReq, callback=self.parse,
                                     dont_filter=False,
                                     meta={"goodreadsid":goodreadsid,"cudosid":cudosid})

    # def start_requests(self):
    #     x="3	https://www.goodreads.com/book/show/17401103	Goldilocks and the Three Bears	Sarah Delmege"
    #     datas=x.strip().split("\t")
    #     cudosid = int(datas[0])
    #     goodreadsid = int(datas[1].replace("https://www.goodreads.com/book/show/", ""))
    #     goodreadsReq=datas[1]+"."+"_".join(i for i in datas[2].split(" "))
    #     yield scrapy.Request(goodreadsReq, callback=self.parse,
    #                          dont_filter=False,
    #                          meta={"goodreadsid":goodreadsid,"cudosid":cudosid})

    def parse(self, response):
        score = response.xpath(XpathRule.score).extract()[0].strip()
        reviews = response.xpath(XpathRule.reviews).extract()[0].strip()
        ratings = response.xpath(XpathRule.ratings).extract()[0].strip()
        title = response.xpath(XpathRule.title).extract()[0].strip()
        Tllist = []
        Tlluser = []
        authorUrlList = []
        authorList = []
        for authorInfo in response.xpath(XpathRule.authorName__container).extract():
            authorInfo = etree.fromstring(authorInfo)
            greyText = authorInfo.xpath(".//span[contains(@class,'greyText')]/text()")
            if greyText:
                if "Illustrator" in authorInfo.xpath("./span[contains(@class,'greyText')]/text()")[0].strip():
                    Tllist.append(authorInfo.xpath("./a[@class='authorName']/@href")[0].strip())
                    Tlluser.append(authorInfo.xpath("./a[@class='authorName']/span/text()")[0].strip())
                else:
                    authorUrlList.append(authorInfo.xpath("./a[@class='authorName']/@href")[0].strip())
                    authorList.append(authorInfo.xpath("./a[@class='authorName']/span/text()")[0].strip())
            else:
                authorUrlList.append(authorInfo.xpath("./a[@class='authorName']/@href")[0].strip())
                authorList.append(authorInfo.xpath("./a[@class='authorName']/span/text()")[0].strip())

        coverPic = response.xpath(XpathRule.cover).extract()[0].strip()
        description = ",".join(x.strip() for x in response.xpath(XpathRule.description).extract()) \
            if response.xpath(XpathRule.description).extract() else None
        bookFormat = response.xpath(XpathRule.bookFormat).extract()[0].strip() \
            if response.xpath(XpathRule.bookFormat).extract() else None
        ispage = response.xpath(XpathRule.numberOfPages).extract()
        if ispage:
            pages = ispage[0].strip().replace(" pages","")
        else:
            pages = None
        bookDataBox = response.xpath(XpathRule.bookDataBox).extract()
        infoBoxRowTitle = response.xpath(XpathRule.infoBoxRowTitle).extract()
        if "Original Title" in infoBoxRowTitle:
            Original_title = etree.fromstring(bookDataBox[infoBoxRowTitle.index("Original Title")]).xpath("./text()")[0].strip()
        else:
            Original_title = None

        if "ISBN" in infoBoxRowTitle:
            ISBN = etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN")]).xpath("./text()")[0].strip()
            ISBN13 = \
            etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN")]).xpath(XpathRule.isbn)[0].strip() \
                if etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN")]).xpath(XpathRule.isbn) else None
        elif "ISBN13" in infoBoxRowTitle:
            ISBN13 = etree.fromstring(bookDataBox[infoBoxRowTitle.index("ISBN13")]).xpath("./text()")[0].strip()
            ISBN = None
        else:
            ISBN =ISBN13= None

        if "Edition Language" in infoBoxRowTitle:
            Edition_Language = etree.fromstring(bookDataBox[infoBoxRowTitle.index("Edition Language")]).xpath("./text()")[0].strip() \
                if etree.fromstring(bookDataBox[infoBoxRowTitle.index("Edition Language")]).xpath("./text()") else None
        else:
            Edition_Language = None

        if "Literary Awards" in infoBoxRowTitle:
            Literary_Awards = ",".join(x for x in etree.fromstring(bookDataBox[infoBoxRowTitle.index("Literary Awards")]).xpath("./a[@class='award']/text()"))
        else:
            Literary_Awards = None

        details = response.xpath(XpathRule.details).extract()
        if len(details) >= 2:
            a = etree.fromstring(details[1]).xpath("./text()")[0]
            publishedTime = "".join(x.strip() + " " for x in a.split("\n") if x)
            firstPublishedTime = etree.fromstring(details[1]).xpath(XpathRule.greyText)[0].strip().rstrip(")").lstrip("(") \
                if etree.fromstring(details[1]).xpath(XpathRule.greyText) else publishedTime
        elif len(details) == 1:
            a = etree.fromstring(details[0]).xpath("./text()")[0] if etree.fromstring(details[0]).xpath("./text()") else None
            publishedTime = "".join(x.strip() + " " for x in a.split("\n") if x)
            firstPublishedTime = etree.fromstring(details[0]).xpath(XpathRule.greyText)[0].strip().rstrip(")").lstrip("(") \
                if etree.fromstring(details[0]).xpath(XpathRule.greyText) else publishedTime
        else:
            publishedTime = None
            firstPublishedTime = None
        Rating_details = response.xpath(XpathRule.Rating_details).extract()[0].strip()
        renderRatingGraph = re.search("\[(.*?)\]", Rating_details).group(1)
        elementList = response.xpath(XpathRule.elementList).extract()
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
                genres = None
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
        item["ISBN"] = ISBN if ISBN else None
        item["ISBN13"] = ISBN13.lstrip("(ISBN13: ").rstrip(")") if ISBN13 else None
        item["genres"] = str(genres).replace("'", "\'") if genres else None
        item["bookFormat"] = bookFormat.replace("'", "\'") if bookFormat else None
        item["publishedTime"] = publishedTime.replace("'", "\'") if publishedTime else None
        item["firstPublishedTime"] = firstPublishedTime.replace("'", "\'") if firstPublishedTime else None
        item["pages"] = pages if pages else None
        item["originalTitle"] = Original_title.replace("'", "\'") if Original_title else None
        item["literaryAwards"] = Literary_Awards.replace("'", "\'") if Literary_Awards else None
        item["editionLanguage"] = Edition_Language.replace("'", "\'") if Edition_Language else None
        item['description'] = description.replace("'", "\'").replace("\n","") if description else None

        otherEditionsActions=response.xpath("//div[@class='otherEditionsActions']/a[@class='actionLinkLite']/@href").extract()
        if otherEditionsActions:
            actionLinkLite="https://www.goodreads.com"+otherEditionsActions[0]
            yield scrapy.Request(actionLinkLite+"?per_page=100", callback=self.otherLink,dont_filter=False,meta={"goodreadsid":response.meta["goodreadsid"],"item":item})
        else:
            isbninfo = {}
            isbninfo[response.meta["goodreadsid"]]=[ISBN,ISBN13]
            item["isbninfo"]=str(isbninfo) if isbninfo else None
            yield item
            print "-----------",response.meta["goodreadsid"]



    def otherLink(self,response):
        isbninfo={}
        infolist = response.xpath("//div[@class='editionData']").extract()
        for info in infolist:
            info =etree.fromstring(info)
            infoUrl=info.xpath(".//a[@class='bookTitle']/@href")[0].strip()
            infoId=re.search("book/show/(\d+)",infoUrl).group(1)
            if str(infoId) in str(response.meta["goodreadsid"]):
                continue
            moreDetails=info.xpath(".//div[@class='moreDetails hideDetails']")
            for i in moreDetails:
                dataRow=i.xpath("./div[@class='dataRow']")
                # isbninfo[infoId] = [None, None]
                ISBN=None
                ISBN13=None
                language=None
                for data in dataRow:
                    dataTitle=data.xpath("./div[@class='dataTitle']/text()")[0].strip()
                    if "Edition language" in dataTitle:
                        language = data.xpath("./div[@class='dataValue']/text()")[0].strip()
                    if "ISBN13" in dataTitle:
                        ISBN13 = data.xpath("./div[@class='dataValue']/text()")[0].strip().lstrip("(ISBN13: ").rstrip(")")
                        ISBN=None
                        # isbninfo[infoId]=[ISBN, ISBN13.lstrip("(ISBN13: ").rstrip(")")]
                    elif "ISBN" in dataTitle:
                        ISBN=data.xpath("./div[@class='dataValue']/text()")[0].strip()
                        greyText=data.xpath("./div[@class='dataValue']/span[@class='greyText']/text()")[0].strip() if data.xpath("./div[@class='dataValue']/span[@class='greyText']/text()") else None
                        ISBN13 = greyText.lstrip("(ISBN13: ").rstrip(")") if greyText else None
                        # isbninfo[infoId]=[ISBN,ISBN13.lstrip("(ISBN13: ").rstrip(")") if ISBN13 else None]
            isbninfo[infoId]=[ISBN,ISBN13,language]

        item=response.meta["item"]
        item["isbnInfo"]=str(isbninfo) if isbninfo else None
        print "\n--------------------图书字段信息-------------------"
        print "   cudosid  :" + str(item["cudosid"])
        print "   goodreadsId  :" + str(item["goodreadsId"])
        print "   goodreadsUrl    :" + item["goodreadsUrl"]
        print "   title    :" + item["title"]
        print "   authorName    :" + item["authorName"]
        print "   authorNameUrl    :" + item["authorNameUrl"]
        print "   Illustrator   :" + str(item["Illustrator"])
        print "   IllustratorUrl   :" + str(item["IllustratorUrl"])
        print "   coverPic    :" + item["coverPic"]
        print "   ratingDetails    :" + item["ratingDetails"]
        print "   score    :" + item["score"]
        print "   ratings    :" + item["ratings"]
        print "   reviews    :" + item["reviews"]
        print "   genres     :" + str(item["genres"])
        print "   bookFormat    :" + str(item["bookFormat"])
        print "   publishedTime    :" + str(item["publishedTime"])
        print "   firstPublishedTime    :" + str(item["firstPublishedTime"])
        print "   pages    :" + str(item["pages"])
        print "   ISBN    :" + str(item["ISBN"])
        print "   ISBN13    :" + str(item["ISBN13"])
        print "   originalTitle    :" + str(item["originalTitle"])
        print "   literaryAwards   :" + str(item["literaryAwards"])
        print "   editionLanguage    :" + str(item["editionLanguage"])
        print "   description    :" + str(item["description"])
        print "   isbnInfo    :" + str(isbninfo)
        print "--------------------图书字段信息-------------------\n"
        yield item













