# -*- coding: utf-8 -*-

import advancedclassify

ageonly = advancedclassify.loadmatch('agesonly.csv', allnum=True)
matchmaker = advancedclassify.loadmatch('matchmaker.csv')
#print ageonly
#print matchmaker

advancedclassify.plotagematches(ageonly)