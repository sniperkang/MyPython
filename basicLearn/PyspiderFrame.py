#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-11-29 15:19:33
# Project: CNVD_Spider

from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysqldb import ToMySQL

PageNumber = 3
StartUrl = 'http://ics.cnvd.org.cn/?max=1&offset=' + str(PageNumber)

ConString = {
    'host':'localhost',
    'user':'root',
    'passwd':'sniperkang',
    'db':'test',
    'charset':'utf8'
}

Headers1 = [
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Encoding', 'gzip, deflate'),
    ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
    ('Connection', 'keep-alive'),
    ('Cookie', '__jsluid=cd22b5cf5aeaa05ef144c68a0c8b6fd8; FSSBBIl1UgzbN7N80T=1uiiCPKGLGkvcJl5Y1_SN0SCS.QTblWKLIQ8Y_Ws7tr_iXhWhjSxumd2Sg6ZEPdfgdm9BHvWu4w6zqUQMbZvTGoYpbo5PhOgkkCxA5DmOnghRc1PjSEcurCjqt68gTm_lF7ca4dkOHn66I4nj8qKKBzQvujUDhLvAtpMMCzIBoDIg3wcO3jmumB.W6m8pLoYx1GF8Vq9_lsvLAUopV7ut7cc0eVNePI5TaJp9..79z.my3HkiCf9G9xFE5oH.8RkvFaCYt.c1cPozUajWHVkJvZGTuJYlePxeUEgnNfnqpIni; FSSBBIl1UgzbN7N80S=RXKiYETFlDnDSZ2vL83Ic4T5eLDV4WM2Dx.t_MoM95EBF2CtLyDmaWG0IiSefc3x; bdshare_firstime=1480406828376; __jsl_clearance=1480493552.839|0|6tq%2BUIi8Y2XzjTNBG8xcUAsAtcA%3D; JSESSIONID=A1D4F846D2093AF37C39BD2A58246B34'),
    ('Referer', StartUrl),
    ('Upgrade-Insecure-Requests', '1'),
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
]

Headers2 = [
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Encoding', 'gzip, deflate'),
    ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
    ('Connection', 'keep-alive'),
    ('Cookie', '__jsluid=fabe0b42b024cf678a08a53ce857caf8'),
    ('Host', 'ics.cnvd.org.cn'),
    ('Upgrade-Insecure-Requests', '1'),
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
]

class Handler(BaseHandler):
    crawl_config = {
        "headers": {
            "User-Agent": "BaiDuSpider", #配置用户代理，模拟百度蜘蛛
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        print 1
        self.crawl(StartUrl, callback=self.index_page)
#        self.crawl(StartUrl, callback=self.detail_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        print 2
        self.crawl(StartUrl, callback=self.list_page)
#        self.list_page = StartUrl
#        for each in response.doc('a[href^="http"]').items():
#        for each in response.doc('html>body>div.con>div.con_left>div.list>table>tbody#tr>tr>td>a').items():
#            self.crawl(each.attr.href, callback=self.detail_page)
#            a=each.attr.href.replace('www','ics')
#            self.crawl(a,callback=self.list_page, headers=Headers)
#            self.crawl(each.attr.href,callback=self.list_page, headers=Headers)
#            self.crawl(each.attr.href,callback=self.detail_page)

    @config(age=10*24*60*60)
    def list_page(self,response):
        print 3
#获得漏洞详细内容链接并交给下一个函数处理
        for each in response.doc('html>body>div.con>div.con_left>div.list>table>tbody#tr>tr>td>a').items():
#        for each in response.doc('a[href^="http"]').items():
            print each
#            self.crawl(each.attr.href,callback=self.detail_page, headers=Headers1)
            self.crawl(each.attr.href,callback=self.detail_page)
#翻页，然后继续由list_page函数处理
        for each in response.doc('html>body>div.con>div.con_left>div.list>div.pages.clearfix>a.nextLink').items():
#        for each in response.doc('a[href^="http"]').items():
#            print each
            self.crawl(each.attr.href,callback=self.list_page, headers=Headers2)

    @config(priority=2)
    def detail_page(self, response):
        print 4
        return {
            "url": response.url,
            "title":response.doc('html>body>div.mw.Main.clearfix>div.blkContainer>div.blkContainerPblk>div.blkContainerSblk>h1').text(),
            "cnvdid":response.doc('html>body>div.mw.Main.clearfix>div.blkContainer>div.blkContainerPblk>div.blkContainerSblk>div.blkContainerSblkCon.clearfix>div.tableDiv>table.gg_detail>tbody>tr>td').eq(1).text()
        }

    def on_result(self, result):
        print 5
        if not result or not result['title']:
            return
        sql = ToMySQL()
        print result
        sql.insert(self,**result)


