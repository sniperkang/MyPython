#-*- coding: utf-8 -*-

import urllib2
import searchengine

c = urllib2.urlopen('http://kiwitobes.com/wiki/Programming_language.html')
content = c.read()
print content[0 : 50]

crawler = searchengine.crawler('searchindex.db')
crawler.createindextables()