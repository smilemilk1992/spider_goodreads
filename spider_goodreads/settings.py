# -*- coding: utf-8 -*-

# Scrapy settings for spider_goodreads project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider_goodreads'

SPIDER_MODULES = ['spider_goodreads.spiders']
NEWSPIDER_MODULE = 'spider_goodreads.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spider_goodreads (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
COOKIES_ENABLED=True
RETRY_ENABLED=True
HTTPERROR_ALLOWED_CODES = [403,302,301,503,502,504,307,500]
RETRY_HTTP_CODES = [403,500, 502, 503, 504, 522, 524, 408,302,301,307]
# LOG_FILE = "mySpider.log"
# LOG_LEVEL = "DEBUG"
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False
# LOG_LEVEL="INFO"
# LOG_FILE="goodreads"
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language':'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Cookie':'csid=BAhJIhg5ODQtNDI1NzIwNi05MzI3NTA4BjoGRVQ%3D--22423b42a913370ac8cc7af728d2202b6ca25656; locale=zh; _session_id2=09e76bbd2be17e8439c0edb0eae3570b; __utmc=250562704; __utmz=250562704.1562980557.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=48455b7ec2b50b5d:T=1562980558:S=ALNI_MZlZ0i1R5h18YIh59tSPCIGfbx3Zw; __qca=P0-1661288274-1562980560171; csm-sid=502-7843117-3474024; never_show_interstitial=true; __utma=250562704.782759257.1562980557.1563068939.1563073825.11; __utmt=1; __utmb=250562704.1.10.1563073825'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'spider_goodreads.middlewares.SpiderGoodreadsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'spider_goodreads.middlewares.SpiderGoodreadsDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'spider_goodreads.pipelines.SpiderGoodreadsPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
