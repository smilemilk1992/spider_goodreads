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
        'CONCURRENT_REQUESTS': 6,  #允许的线程数
        'RETRY_TIMES': 3,  #重试机制
        'DOWNLOAD_DELAY':1,   #延时（秒）
        # 'ITEM_PIPELINES': {
        #     "spider_goodreads.pipelines.pipelines_library.SpiderGoodreadsPipeline": 200,
        # },
        'DOWNLOADER_MIDDLEWARES': {
            'spider_goodreads.middlewares.RandomUserAgent.RandomUserAgent': 300,
            # 'spider_goodreads.middlewares.random_http_proxy.IpMiddleware': 110, #添加代理ip逻辑
        },

    }



    flagUrl="https://www.worldcat.org/wcpa/servlet/org.oclc.lac.ui.ajax.ServiceServlet?serviceCommand=librarySearch&search={}&start=1&count=10000&libType=none&dofavlib=false&sort=none"



    def start_requests(self):
        with open('zipcode.txt', "r") as f:
            url = f.readlines()
            for x in url:
                datas=x.strip().split("\t")
                name = datas[0]
                Abbreviation=datas[1]
                link=self.flagUrl.format(name)
                yield scrapy.Request(link, callback=self.parse,meta={"Abbreviation": Abbreviation, "name": name})


    def parse(self, response):
        links = response.xpath("//table[@id='libsresults']//p[@class='lib']/a/@href").extract()
        libsearchaddress=response.xpath("//table[@id='libsresults']//p[@class='lib-search-address']").extract()
        for link in links:
            libsearch = etree.fromstring(libsearchaddress[links.index(link)].replace("<br>", "").encode("utf-8")).xpath("./text()")[0]

            infos=re.split("\n|,",libsearch.replace(u"\xa0","").strip())
            url = "https://www.worldcat.org"+link

            print infos,url
            # yield scrapy.Request(url, callback=self.getInfo, meta={"Abbreviation": response.meta['Abbreviation'], "name": response.meta['name']})

    def getInfo(self,response):
        libdata="//div[@id='lib-data']"
        title = response.xpath(libdata+"//h1/text()").extract_first().strip().replace("\n","").replace("#1","")
        psdata = response.xpath(libdata+"//p").extract()
        for p in psdata:
            p=etree.HTML(p)
            print p.xptah(".//text()")[0]


