#-*- coding: utf-8 -*-

from PIL import Image,ImageDraw

def readfile(filename):
  # 每一行为list的一个元素
  lines=[line for line in file(filename)]

  # 第一行是列标题 lines的第一个元素
  # 删除首尾'\n','\r','\t',' '等空字符，用tab分隔
  # First line is the column titles
  #print lines
  colnames=lines[0].strip().split('\t')[1:]
  #print lines[0]
  #print colnames
  #print lines[1:]
  rownames=[]
  data=[]
  # lines的后n-1行为n-1个p元素
  for line in lines[1:]:
    p=line.strip().split('\t')
    #print line
    #print p
    # p的第一列为行名
    # 每行的第一列是行名
    # First column in each row is the rowname
    rownames.append(p[0])
    #print rownames
    # 剩余的部分就是该行对应的数据
    # The data for this row is the remainder of the row
    data.append([float(x) for x in p[1:]])
    #print data
  return rownames,colnames,data


from math import sqrt

# 计算皮尔逊相关度 完全匹配为1.0 毫无关系为0.0 1.0-相关度 相似度越大 距离越小
def pearson(v1,v2):
  # 简单求和
  # Simple sums
  sum1=sum(v1)
  sum2=sum(v2)

  # 求平方和
  # Sums of the squares
  sum1Sq=sum([pow(v,2) for v in v1])
  sum2Sq=sum([pow(v,2) for v in v2])	

  # 求乘积之和
  # Sum of the products
  pSum=sum([v1[i]*v2[i] for i in range(len(v1))])

  # 计算r（Pearson score）
  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/len(v1))
  den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
  if den==0: return 0

  return 1.0-num/den

# “聚类”类
class bicluster:
  def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
    self.left=left
    self.right=right
    self.vec=vec
    self.id=id
    self.distance=distance

# 分级聚类算法
# 尝试每一组可能的配对并计算相关度，找出最佳配对
# 最佳配对的两个聚类被合并成一个新的聚类
def hcluster(rows,distance=pearson):
  distances={}
  currentclustid=-1

  # 最开始的聚类就是数据集中的行
  # clust是以len(rows)个（即调用时的len（data）个，如3）
  # 来自rows（即调用时的data）行向量作为vec参数形成的
  # bicluster对象构成的list
  # Clusters are initially just the rows
  clust=[bicluster(rows[i],id=i) for i in range(len(rows))]
  #print clust[0].vec

  # 重复进行聚类操作，直到只剩下一个聚类为止
  while len(clust)>1:
    # 假设初值
    lowestpair=(0,1)
    closest=distance(clust[0].vec,clust[1].vec)

    # 遍历每一个配对，寻找最小距离
    # loop through every pair looking for the smallest distance
    for i in range(len(clust)):
      # 两两成对遍历
      for j in range(i+1,len(clust)):
        # 用distances来缓存距离的计算值
        # distances为以2维tuple为key的dict
        # key为tuple保证唯一性
        # distances is the cache of distance calculations
        #print distances
        #print (clust[i].id,clust[j].id)
        # distance(clust[i].vec,clust[j].vec)为以pearson等算法计算两向量距离
        if (clust[i].id,clust[j].id) not in distances: 
          distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)

        d=distances[(clust[i].id,clust[j].id)]

        # 最小距离
        if d<closest:
          closest=d
          lowestpair=(i,j)

    # 计算两个聚类的平均值
    # calculate the average of the two clusters
    #print lowestpair
    #print lowestpair[0]
    #print lowestpair[1]
    # lowestpair为元组，其元素标识了最近的2个聚类的id
    mergevec=[
    (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 
    for i in range(len(clust[0].vec))]

    # 建立新的聚类
    # create the new cluster
    newcluster=bicluster(mergevec,left=clust[lowestpair[0]],
                         right=clust[lowestpair[1]],
                         distance=closest,id=currentclustid)

    # 不在原始集合中的聚类，其id为负数
    # 发生第一次聚类前初值为-1，发生后更新
    # cluster ids that weren't in the original set are negative
    currentclustid-=1
    #print len(clust)
    # 删除旧聚类
    del clust[lowestpair[1]]
    del clust[lowestpair[0]]
    #print len(clust)
    # 添加新聚类
    clust.append(newcluster)

  return clust[0]

# 递归遍历聚类树，将其以类似文件系统层级结构的形式打印出来
def printclust(clust,labels=None,n=0):
  #print 1
  # 利用缩进来建立层级布局
  # indent to make a hierarchy layout
  for i in range(n): print ' ',
  if clust.id<0:
    # 负数标记代表这是一个分支
    # negative id means that this is branch
    print '-'
  else:
    # 正数标记代表这是一个叶节点
    # positive id means that this is an endpoint
    if labels==None: print clust.id
    else: print labels[clust.id]

  # 现在开始打印右侧分支和左侧分支
  # now print the right and left branches
  # 此处将左侧分支及其下枝叶全部打印，此处为递归，递归完子分支返回上一级
  if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
  # 此处将右侧分支及其下枝叶全部打印，此处为递归，递归完子分支返回上一级
  if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)

# 聚类总体高度
def getheight(clust):
  # 这是一个叶节点吗？若是，则高度为1
  # Is this an endpoint? Then the height is just 1
  if clust.left==None and clust.right==None: return 1

  # 否则，高度为每个分支的高度之和
  # Otherwise the height is the same of the heights of
  # each branch
  return getheight(clust.left)+getheight(clust.right)

# 聚类根节点总体误差深度
def getdepth(clust):
  # The distance of an endpoint is 0.0
  if clust.left==None and clust.right==None: return 0

  # The distance of a branch is the greater of its two sides
  # plus its own distance
  return max(getdepth(clust.left),getdepth(clust.right))+clust.distance


# 为每个聚类生成高度为20像素、宽度固定的图片
# 缩放因子是由由固定宽度除以总的深度值得到
# 函数为图片建立draw对象，并在根节点位置调用drawnode
# 令其处于整幅图片左侧正中间
def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
  # 高度和宽度
  # height and width
  h=getheight(clust)*20
  w=1200
  depth=getdepth(clust)

  # 由于宽度是固定的，因此我们须要对距离值做相应的调整
  # width is fixed, so scale distances accordingly
  scaling=float(w-150)/depth

  # 新建一个白色背景的图片
  # Create a new image with a white background
  img=Image.new('RGB',(w,h),(255,255,255))
  draw=ImageDraw.Draw(img)

  draw.line((0,h/2,10,h/2),fill=(255,0,0))    

  # 画第一个点
  # Draw the first node
  drawnode(draw,clust,10,(h/2),scaling,labels)
  img.save(jpeg,'JPEG')

# 以聚类及其位置为输入，用子节点高度计算其位置并将其连接
# 包括一条长垂直线及两条水平线，水平线长度与误差值成正比
def drawnode(draw,clust,x,y,scaling,labels):
  if clust.id<0:
    h1=getheight(clust.left)*20
    h2=getheight(clust.right)*20
    top=y-(h1+h2)/2
    bottom=y+(h1+h2)/2
    # 线的长度
    # Line length
    ll=clust.distance*scaling
    # 聚类到其子节点的垂直线
    # Vertical line from this cluster to children    
    draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))    

    # 连接左侧节点的水平线
    # Horizontal line to left item
    draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))    

    # 连接右侧节点的水平线
    # Horizontal line to right item
    draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))        

    # 调用函数绘制左右节点
    # Call the function to draw the left and right nodes    
    drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
    drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
  else:
    # 如果这是一个叶节点，则绘制节点的标签
    # If this is an endpoint, draw the item label
    draw.text((x+5,y-7),labels[clust.id],(0,0,0))

# 行列转置
def rotatematrix(data):
  newdata=[]
  for i in range(len(data[0])):
    newrow=[data[j][i] for j in range(len(data))]
    newdata.append(newrow)
  return newdata

import random

def kcluster(rows,distance=pearson,k=4):
  # Determine the minimum and maximum values for each point
  ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows])) 
  for i in range(len(rows[0]))]

  # Create k randomly placed centroids
  clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] 
  for i in range(len(rows[0]))] for j in range(k)]
  
  lastmatches=None
  for t in range(100):
    print 'Iteration %d' % t
    bestmatches=[[] for i in range(k)]
    
    # Find which centroid is the closest for each row
    for j in range(len(rows)):
      row=rows[j]
      bestmatch=0
      for i in range(k):
        d=distance(clusters[i],row)
        if d<distance(clusters[bestmatch],row): bestmatch=i
      bestmatches[bestmatch].append(j)

    # If the results are the same as last time, this is complete
    if bestmatches==lastmatches: break
    lastmatches=bestmatches
    
    # Move the centroids to the average of their members
    for i in range(k):
      avgs=[0.0]*len(rows[0])
      if len(bestmatches[i])>0:
        for rowid in bestmatches[i]:
          for m in range(len(rows[rowid])):
            avgs[m]+=rows[rowid][m]
        for j in range(len(avgs)):
          avgs[j]/=len(bestmatches[i])
        clusters[i]=avgs
      
  return bestmatches

def tanamoto(v1,v2):
  c1,c2,shr=0,0,0
  
  for i in range(len(v1)):
    if v1[i]!=0: c1+=1 # in v1
    if v2[i]!=0: c2+=1 # in v2
    if v1[i]!=0 and v2[i]!=0: shr+=1 # in both
  
  return 1.0-(float(shr)/(c1+c2-shr))

def scaledown(data,distance=pearson,rate=0.01):
  n=len(data)

  # The real distances between every pair of items
  realdist=[[distance(data[i],data[j]) for j in range(n)] 
             for i in range(0,n)]

  # Randomly initialize the starting points of the locations in 2D
  loc=[[random.random(),random.random()] for i in range(n)]
  fakedist=[[0.0 for j in range(n)] for i in range(n)]
  
  lasterror=None
  for m in range(0,1000):
    # Find projected distances
    for i in range(n):
      for j in range(n):
        fakedist[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2) 
                                 for x in range(len(loc[i]))]))
  
    # Move points
    grad=[[0.0,0.0] for i in range(n)]
    
    totalerror=0
    for k in range(n):
      for j in range(n):
        if j==k: continue
        # The error is percent difference between the distances
        errorterm=(fakedist[j][k]-realdist[j][k])/realdist[j][k]
        
        # Each point needs to be moved away from or towards the other
        # point in proportion to how much error it has
        grad[k][0]+=((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
        grad[k][1]+=((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm

        # Keep track of the total error
        totalerror+=abs(errorterm)
    print totalerror

    # If the answer got worse by moving the points, we are done
    if lasterror and lasterror<totalerror: break
    lasterror=totalerror
    
    # Move each of the points by the learning rate times the gradient
    for k in range(n):
      loc[k][0]-=rate*grad[k][0]
      loc[k][1]-=rate*grad[k][1]

  return loc

def draw2d(data,labels,jpeg='mds2d.jpg'):
  img=Image.new('RGB',(2000,2000),(255,255,255))
  draw=ImageDraw.Draw(img)
  for i in range(len(data)):
    x=(data[i][0]+0.5)*1000
    y=(data[i][1]+0.5)*1000
    draw.text((x,y),labels[i],(0,0,0))
  img.save(jpeg,'JPEG')  
