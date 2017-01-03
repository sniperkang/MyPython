# -*- coding: utf-8 -*-

import treepredict

#print treepredict.divideset(treepredict.my_data, 2, 'yes')
#print treepredict.divideset(treepredict.my_data, 0, 'google')

#print treepredict.giniimpurity(treepredict.my_data)
#print treepredict.entropy(treepredict.my_data)

#set1, set2 = treepredict.divideset(treepredict.my_data, 2, 'yes')
#print treepredict.entropy(set1)
#print treepredict.giniimpurity(set1)

tree = treepredict.buildtree(treepredict.my_data)
#print tree
treepredict.printtree(tree)