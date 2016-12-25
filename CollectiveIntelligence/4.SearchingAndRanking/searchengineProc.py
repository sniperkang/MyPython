# -*- coding: utf-8 -*-

import urllib2
import searchengine

#c = urllib2.urlopen('https://en.wikipedia.org/wiki/Programming_language')
#content = c.read()
#print content[0 : 50]
#print content

#pagelist = ['https://en.wikipedia.org/wiki/Programming_language']
#crawler = searchengine.crawler('')
#crawler.crawl(pagelist)

crawler = searchengine.crawler('searchindex.db')
crawler.createindextables()
pages = ['https://en.wikipedia.org/wiki/Programming_language']
crawler.crawl(pages)

import nn

#mynet = nn.searchnet('nn.db')
#mynet.maketables()
#wWorld, wRiver, wBank = 101, 102, 103
#uWorldBank, uRiver, uEarth = 201, 202, 203
#mynet.generatehiddennode([wWorld, wBank],[uWorldBank, uRiver, uEarth])
#for c in mynet.con.execute('SELECT * FROM wordhidden'): print c
#for c in mynet.con.execute('SELECT * FROM hiddenurl'): print c
