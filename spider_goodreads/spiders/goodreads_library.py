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
        'DEFAULT_REQUEST_HEADERS' : {
            'Referer':'https://www.worldcat.org/title/knuffle-bunny-a-cautionary-tale/oclc/1083732673?loc=94404',
            'Cookie':'owcFirstDiscoveryRedir=promptUserFirstTime; owcLocRedirectSession=_nr.no_inst; JSESSIONID=F4376BE187CC125CD8877B5302F55B46; showhide-cite-link=-1c; __atuvc=1%7C28; LAC-User-Query=su%3ACamps+Juvenile+fiction.; LAC-User-FacetedQuery=; LAC-SR-Url=/search?q=su%3ACamps+Juvenile+fiction.&fq=&dblist=638&start=1; selected_check_boxes=; fm_facet_start=; fm_facet_se=; fm_facet_sd=; LAC-User-Location=94404; LAC-User-DisplayLocation=%E7%BE%8E%E5%9B%BD%E5%8A%A0%E5%88%A9%E7%A6%8F%E5%B0%BC%E4%BA%9A%E5%B7%9E%E7%A6%8F%E6%96%AF%E7%89%B9%E5%9F%8E%E9%82%AE%E6%94%BF%E7%BC%96%E7%A0%81%3A+94404; LAC-User-Geocode=37.5549479%2C-122.2710602; owc-holding-state="1& & "; TS015377c2=011e52333529e5a499b551cd574c4b3418cf7f1f751824403ebf4128720da3e8af96e2ced50985f46ce7a207649d699941712dad9cb56a24f5b0e811e7a9d91b03bb37f9dafc205aba2ddfc6a4c7a65dfbfaf7dce83b68ae8578e23e331f173c12e79edf3233124fdf09833aad300d122e58221f51bfbaf206652e93bdbef4efe5621a55f532d72f0453d09603776c490b39288fd32fbca2f65dfa2adc31bc397fc557bda6da33bd6dfcc3c1fd571a08f066e20f1bf738bd7e42eac69e3c5943d54dfc2d8a8f305ab2798cc64e574f86a2cb35f5ff'
        }
    }




# https://www.goodreads.com/author/list/93621.Ellen_Jackson   作者书籍清单
    #开始种子URL
    # start_urls = ['https://www.goodreads.com/book/show/16077840-el-creador']

    start_url="https://www.worldcat.org/wcpa/servlet/org.oclc.lac.ui.ajax.ServiceServlet?wcoclcnum=1083732673&start_holding={}&serviceCommand=holdingsdata"
    def start_requests(self):
        n=1
        page=6*(n-1)+1
        url = self.start_url.format(page)
        yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
        print response.body
        title=response.xpath("//div[@class='dropdiv2-util-int']/b/text()").extract()
        for t in title:
            print t