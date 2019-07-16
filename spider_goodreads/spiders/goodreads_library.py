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
    name = "goodreads_library"
    custom_settings = {
        'CONCURRENT_REQUESTS': 36,  #允许的线程数
        'RETRY_TIMES': 3,  #重试机制
        'DOWNLOAD_DELAY':1,   #延时（秒）
        'ITEM_PIPELINES': {
            "spider_goodreads.pipelines.pipelines_library.SpiderGoodreadsPipeline": 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'spider_goodreads.middlewares.RandomUserAgent.RandomUserAgent': 300,
            # 'spider_goodreads.middlewares.random_http_proxy.IpMiddleware': 110, #添加代理ip逻辑
        },

    }







# https://www.goodreads.com/author/list/93621.Ellen_Jackson   作者书籍清单
    #开始种子URL
    # start_urls = ['https://www.goodreads.com/book/show/16077840-el-creador']

    start_url="https://www.worldcat.org/wcpa/servlet/org.oclc.lac.ui.ajax.ServiceServlet?wcoclcnum=1083732673&start_holding={}&serviceCommand=holdingsdata"
    def start_requests(self):
        n=1
        page=6*(n-1)+1
        url = self.start_url.format(page)
        yield scrapy.Request(url, callback=self.parse,cookies={'LAC-User-Location':94404},meta={"page":1})


    def parse(self, response):
        libsresults=response.xpath("//table[@id='libsresults']//td[@class='name']").extract()
        for lib in libsresults:
            if re.search('href="(.*?)"',str(lib)):
                url ="https://www.worldcat.org"+re.search('href="(.*?)"',str(lib)).group(1)
                name=re.search('">(.*?)</a>',str(lib)).group(1).replace("<a>","")
                info = re.search('"geoloc">(.*?)<',str(lib)).group(1).split(",")
                info1=info[1].split(" ")
                item={}
                item["OriginalUrl"] = response.url

                item["libName"]=name
                item["city"]=info[0]
                item["CA"]=info1[1]
                item["postal"]=info1[2]
                item["Country"]=" ".join(x for x in info1[3:])

                yield scrapy.Request(url.replace("amp;",""), callback=self.info, cookies={'LAC-User-Location': 94404}, meta={"item": item})


        if libsresults:
            page=response.meta["page"]+1
            url = self.start_url.format(6 * (page - 1) + 1)
            yield scrapy.Request(url, callback=self.parse, cookies={'LAC-User-Location': 94404},meta={"page": page})


    def info(self,response):
        item=response.meta["item"]
        item["libUrl"] = response.url
        yield item
