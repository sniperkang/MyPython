#-*- coding: utf-8 -*-

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
pages = ['https://en.wikipedia.org/wiki/Progarmming_language']
crawler.crawl(pages)
