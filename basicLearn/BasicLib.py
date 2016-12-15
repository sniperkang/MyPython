# -*- coding:utf-8 -*-
#coding = utf-8
import urllib
import urllib2
import re
import random
import socket
import MySQLdb as mdb
import cookielib

pagenumber=0
url = 'http://ics.cnvd.org.cn/?max=100&offset='+str(pagenumber)
# url='http://www.cnvd.org.cn/flaw/show/CNVD-2016-05694'

cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
urllib2.install_opener(opener)
opener2= urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
urllib2.install_opener(opener2)

user_agents = [
             'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
             'Opera/9.25 (Windows NT 5.1; U; en)',
             'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
             'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
             'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
             'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
             "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
             "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
             "Mozilla-Firefox-Spider(Wenanry)"
             ]

agent = random.choice(user_agents)

UserAgent = "Mozilla-Firefox-Spider(Wenanry)"

opener.addheaders = [("User-agent",UserAgent),("Accept","*/*"),('Referer','http://www.miit.gov.cn/')]

con = mdb.connect('127.0.0.1', 'root', 'root', 'test', port=3307,charset="utf8");
with con:
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS \
        BUGnews(Id INT PRIMARY KEY AUTO_INCREMENT, WebUrl VARCHAR(50))")
    try:
        res = opener.open(url)
        content= res.read()
#         request = urllib2.Request(url,headers = header1)
#         response = urllib2.urlopen(request)
#         content= response.read().decode('utf-8')

        print content
        pattern= re.compile('<a.*?href="(.*?)" title=',re.S)
        items= re.findall(pattern,content)
        for item in items:
            url2=item
#             opener2.addheaders = [("User-agent","Mozilla-Firefox-Spider(Wenanry)"),("Accept","*/*"),('Referer','http://www.google.com')]
#             res2=opener2.open(url2)
#             contentnews= res2.read()
#             print contentnews
            sql="insert into BUGnews(WebUrl) VALUES (%s)"
            params=item.encode('utf-8')
            cur.execute(sql,params)
    #         res2 = opener2.open(url2)
    #         content2= res2.read()
    #         print content2

    except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason


