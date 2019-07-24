# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import MySQLdb
from concurrent.futures import ThreadPoolExecutor
def start():
    with open('cudos_goodreads.txt', "r") as f:
        url = f.readlines()
        with ThreadPoolExecutor(10) as executor:
            for x in url:
                datas = x.split("\t")
                executor.submit(getInfo, datas)



def getInfo(datas):
    cudosId = datas[0]
    goodreadsUrl = datas[1]
    title = datas[2]
    link = goodreadsUrl + "." + "_".join(x for x in title.split(" "))
    goodreadsId = goodreadsUrl.replace("https://www.goodreads.com/book/show/", "")
    rs = requests.get(link)
    soup = BeautifulSoup(rs.text,"html.parser")
    OnlineStores = soup.find("div",{"class":"floatingBox buyBox"}).find_all("a",{"class":"actionLinkLite"})
    stores={}
    for i in OnlineStores:
        key=i.get_text()
        value="https://www.goodreads.com"+i['href']
        stores[key]=value
    goodreadsAmazonUrl = "https://www.goodreads.com" + \
                         soup.find("a", id="buyButton")["href"]
    goodreadsAlibrisUrl=stores["Alibris"].split("&")[0]
    goodreadsWalmarteBooksUrl=stores["Walmart eBooks"].split("&")[0]
    goodreadsBarnesNoble=stores["Barnes & Noble"].split("&")[0]
    goodreadsIndieBound=stores["IndieBound"].split("&")[0]
    goodreadsIndigo=stores["Indigo"].split("&")[0]

    AmazonUrl = requests.get(goodreadsAmazonUrl).url.split("ref=")[0]
    AlibrisUrl=requests.get(goodreadsAlibrisUrl).url.split("&")[0]
    WalmarteBooksUrl = requests.get(goodreadsWalmarteBooksUrl).url.split("&")[0]
    BarnesNoble = "https://www.barnesandnoble.com/w/?ean="+requests.get(goodreadsBarnesNoble).url.split("&")[0].split("?ean=")[1]
    IndieBound=requests.get(goodreadsIndieBound).url
    Indigo=requests.get(goodreadsIndigo).url
    print link,AmazonUrl,AlibrisUrl,WalmarteBooksUrl,BarnesNoble,IndieBound,Indigo

    print "---------------"

def insertDb(item):
    sql = '''INSERT IGNORE into p_news_snapshot2(cudosId,goodreadsId,title,goodreadsUrl,goodreadsReq,goodreadsAmazonUrl,goodreadsAlibrisUrl,goodreadsWalmarteBooksUrl,goodreadsBarnesNoble,goodreadsIndieBound,goodreadsIndigo)value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    conn = MySQLdb.connect(
        host='120.27.218.142',
        port=3306,
        user='worker',
        passwd='worker',
        db='test',
        charset="utf8"
    )
    cur = conn.cursor()
    insertdata = (
        item['cudosId'],
        item['goodreadsId'],
        item['title'],
        item['goodreadsUrl'],
        item['goodreadsReq'],
        item['goodreadsAmazonUrl'],
        item['goodreadsAlibrisUrl'],
        item['goodreadsWalmarteBooksUrl'],
        item['goodreadsBarnesNoble'],
        item['goodreadsIndieBound'],
        item['goodreadsIndigo']
    )
    cur.execute(sql, insertdata)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    start()