#encoding:utf-8
import MySQLdb
from scrapy.cmdline import execute
execute("scrapy crawl goodreads_snapshot".split())
