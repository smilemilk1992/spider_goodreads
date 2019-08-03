# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
import re
import logging
class XpathRule(object):
    bookDataBox = "//div[@class='clearFloats']/div[@class='infoBoxRowItem']"
    details="//div[@id='details']/div[@class='row']"
    infoBoxRowTitle="//div[@class='clearFloats']/div[@class='infoBoxRowTitle']/text()"


class LibrarySpider(scrapy.Spider):
    '''
    图书信息
    '''
    name = "goodreads_lib"
    custom_settings = {
        'CONCURRENT_REQUESTS': 3,  #允许的线程数
        'RETRY_TIMES': 3,  #重试机制
        # 'DOWNLOAD_DELAY':1,   #延时（秒）
        'ITEM_PIPELINES': {
            "spider_goodreads.pipelines.pipelines_lib.SpiderGoodreadsPipelineCSV": 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'spider_goodreads.middlewares.RandomUserAgent.RandomUserAgent': 300,
            # 'spider_goodreads.middlewares.random_http_proxy.IpMiddleware': 110, #添加代理ip逻辑
        },

    }



    flagUrl="https://www.worldcat.org/wcpa/servlet/org.oclc.lac.ui.ajax.ServiceServlet?serviceCommand=librarySearch&search={}&start=1&count=10000&libType=none&dofavlib=false&sort=none"



    # def start_requests(self):
    #     with open('zipcode.txt', "r") as f:
    #         url = f.readlines()
    #         for x in url:
    #             datas=x.strip().split("\t")
    #             name = datas[0]
    #             Abbreviation=datas[1]
    #             link=self.flagUrl.format(name)
    #             print link
    #             yield scrapy.Request(link, callback=self.parse,dont_filter=False,meta={"Abbreviation": Abbreviation, "name": name})

    def start_requests(self):
        link="https://www.worldcat.org/libraries/90444?backfrom=libraryProfile&searchTerm=Florida&start=1&count=10000&libTypeNum=0&sortBy=ab"
        yield scrapy.Request(link, callback=self.getInfo, dont_filter=False,
                             meta={"Abbreviation": "Florida", "name": "FL"})

    def parse(self, response):
        links = response.xpath("//table[@id='libsresults']//p[@class='lib']/a/@href").extract()
        for link in links:
            url = "https://www.worldcat.org"+link
            yield scrapy.Request(url, callback=self.getInfo, meta={"Abbreviation": response.meta['Abbreviation'], "name": response.meta['name']})

    def getInfo(self,response):
        libdata="//div[@id='lib-data']"
        title = response.xpath(libdata + "//h1/text()").extract_first().strip().replace("\n", "").replace("#1", "")
        psdata = response.xpath(libdata + "//p").extract()
        email = re.search("mailto:(.*?)\"",response.body).group(1) if re.search("mailto:(.*?)\"",response.body) else None
        website=response.xpath("//a[@class='lib-website']/@href").extract()[0] if response.xpath("//a[@class='lib-website']/@href").extract() else None
        if response.xpath(libdata+"/p[@class='lib-alias']").extract():
            p = etree.fromstring(psdata[1].replace("<br>", "\t").encode("utf-8"))
        else:
            p = etree.fromstring(psdata[0].replace("<br>", "\t").encode("utf-8"))
        infos = p.xpath(".//text()")[0].replace(u"\xa0",",,").replace("\n",",,").replace("\s+","").replace("\t","")
        infos=[x.strip() for x in infos.split(",,") if x.strip()]
        print "--",infos
        address = infos[0]
        city = infos[1]
        state=infos[2]
        zipcode=infos[3]
        phone = re.search("\(\d+\) \d+-\d+",response.body).group(0) if re.search("\(\d+\) \d+-\d+",response.body) else None
        item={}
        item["title"]=title
        item["state"]=response.meta["name"]
        item["city"]=city
        item["abbreviation"]=response.meta["Abbreviation"]
        item["zipcode"]=zipcode
        item["email"]=email
        item["website"]=website
        item["worldcatUrl"]=response.url
        item["address"]=address
        item["phone"]=phone
        # print "--------",email,phone,response.url
        print "\n--------------------图书字段信息-------------------"
        print "   title  :" + title
        print "   state  :" + response.meta["name"]
        print "   city    :" + city
        print "   abbreviation    :" + response.meta["Abbreviation"]
        print "   zipcode    :" + zipcode
        print "   email   :" + str(email)
        print "   website   :" + str(website)
        print "   worldcatUrl    :" + response.url
        print "   address    :" + str(address)
        print "   phone    :" + str(phone)
        print "--------------------图书字段信息-------------------\n"
        # yield item



