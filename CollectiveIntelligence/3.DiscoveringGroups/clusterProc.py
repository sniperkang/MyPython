# -*- coding: utf-8 -*-

import clusters

blognames, words, data = clusters.readfile('blogdata.txt')
#print len(data)
# 对data进行聚合
#clust = clusters.hcluster(data)
#print len(clust.vec)
#print clust.id

# 打印聚合树装表格
#clusters.printclust(clust, labels=blognames)

# 绘制聚合树装图
#clusters.drawdendrogram(clust, blognames, jpeg='blogclust.jpg')

# 对data进行转置
#rdata = clusters.rotatematrix(data)
# 对data进行聚合
#wordclust = clusters.hcluster(rdata)
# 绘制聚合树装图
#clusters.drawdendrogram(wordclust, labels=words, jpeg='wordclust.jpg')

# 对data进行K-均值聚类
#kclust = clusters.kcluster(data, k=10)
#print [blognames[r] for r in kclust[0]]
#print [blognames[r] for r in kclust[1]]

"""
import urllib2
from BeautifulSoup import BeautifulSoup
c = urllib2.urlopen('http://www.ibm.com/developerworks/cn/web/1103_zhaoct_recommstudy2/index.html')
soup = BeautifulSoup(c.read())
links = soup('a')
print links[10]
print links[10]['href']
"""
"""
wants, people, data = clusters.readfile('zebo.txt')
clust = clusters.hcluster(data, distance=clusters.tanamoto)
clusters.drawdendrogram(clust, wants)
"""

coords = clusters.scaledown(data)
clusters.draw2d(coords, blognames, jpeg='blogs2d.jpg')