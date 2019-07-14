# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
            "spider_goodreads.pipelines.pipelines.SpiderGoodreadsPipeline": 200,
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
        yield scrapy.Request(url, callback=self.parse,cookies={'LAC-User-Location':94404})


    def parse(self, response):
        libsresults=response.xpath("//table[@id='libsresults']//td[@class='name']").extract()
        for lib in libsresults:
            lib = etree.fromstring(lib)
            # name = etree.fromstring(lib)
            print lib.xpath("/p[@class='geoloc']/text()")