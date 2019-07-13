# -*- coding: utf-8 -*-
import scrapy
import simplejson as json
import time
class XpathRule(object):
    classify = "//div[@class='leftContainer']"
    editor="//span[@class='g-font-size-13 g-color-gray-dark-v4 g-mr-15']/text()"
    peoples="//div[@class='district_box03 w1200 clearfix']//a[@class='forumName']|//div[@class='district_box04 clearfix w1200']//a"
    content="//div[@class='liuyan_box03 w1200 clearfix']/p[@class='zoom']/text()"
    answerContent="//div[@class='clearfix liuyan_box05 w1200']//p[@class='zoom']/text()"


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
    start_urls = ['https://www.goodreads.com/list/show/10762.Best_Book_Boyfriends']

    def parse(self, response):

        title=response.xpath("//h1[@id='bookTitle']/text()").extract()[0].strip()
        authorNameUrl=response.xpath("//a[@class='authorName']/@href").extract()[0].strip()
        authorName = response.xpath("//a[@class='authorName']/span/text()").extract()[0].strip()
        print "   title    :"+title
        print "   authorName    :"+authorName
        print "   authorNameUrl    :"+authorNameUrl



