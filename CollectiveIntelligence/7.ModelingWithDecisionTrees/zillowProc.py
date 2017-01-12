# -*- coding: utf-8 -*-

import zillow
import treepredict

housedata = zillow.getpricelist()
housetree = treepredict.buildtree(housedata, scoref=treepredict.variance)
treepredict.drawtree(housetree, 'housetree.jpg')
