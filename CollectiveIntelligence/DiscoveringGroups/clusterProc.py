# -*- coding: utf-8 -*-

import clusters

blognames, words, data = clusters.readfile('blogdata.txt')
#print len(data)
# 对data进行聚合
clust = clusters.hcluster(data)
#print len(clust.vec)
#print clust.id

# 打印聚合树装表格
#clusters.printclust(clust, labels=blognames)

# 绘制聚合树装图
#clusters.drawdendrogram(clust, blognames, jpeg='blogclust.jpg')

#
rdata = clusters.rotatematrix(data)
wordclust = clusters.hcluster(rdata)
clusters.drawdendrogram(wordclust, labels=words, jpeg='wordclust.jpg')
