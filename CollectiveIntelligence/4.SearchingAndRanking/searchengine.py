# -*- coding: utf-8 -*-

import urllib2
from BeautifulSoup import *
from urlparse import urljoin
from pysqlite2 import dbapi2 as sqlite
import nn
mynet=nn.searchnet('nn.db')

# 构建一个单词列表，这些单词将被忽略
# Create a list of words to ignore
ignorewords={'the':1,'of':1,'to':1,'and':1,'a':1,'in':1,'is':1,'it':1}


class crawler:
  # 初始化crawler类并传入数据库名称
  # Initialize the crawler with the name of database
  def __init__(self,dbname):
    self.con=sqlite.connect(dbname)

  def __del__(self):
    self.con.close()

  def dbcommit(self):
    self.con.commit()

  # 辅助函数，用于获取条目的id，并且如果条目不存在，就将其加入数据库中
  # Auxilliary function for getting an entry id and adding
  # it if it's not present
  def getentryid(self,table,field,value,createnew=True):
    cur=self.con.execute(
    "select rowid from %s where %s='%s'" % (table,field,value))
    res=cur.fetchone()
    if res==None:
      cur=self.con.execute(
      "insert into %s (%s) values ('%s')" % (table,field,value))
      return cur.lastrowid
    else:
      return res[0]


  # 为每个网页建立索引
  # Index an individual page
  def addtoindex(self,url,soup):
    if self.isindexed(url): return
    print 'Indexing '+url

    #
    # Get the individual words
    text=self.gettextonly(soup)
    #print text
    words=self.separatewords(text)
    #print words

    #
    # Get the URL id
    urlid=self.getentryid('urllist','url',url)
    #print urlid

    # Link each word to this url
    for i in range(len(words)):
      word=words[i]
      if word in ignorewords: continue
      wordid=self.getentryid('wordlist','word',word)
      #print wordid
      self.con.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)" % (urlid,wordid,i))


  # 从一个HTML网页中提取文字（不带标签的）
  # Extract the text from an HTML page (no tags)
  def gettextonly(self,soup):
    v=soup.string
    #print soup.contents
    print v
    #if v==Null:
    if v==None:
      c=soup.contents
      resulttext=''
      for t in c:
        #print c
        subtext=self.gettextonly(t)
        resulttext+=subtext+'\n'
      #print resulttext
      return resulttext
    else:
      return v.strip()

  # 根据任何非空白字符进行分词处理
  # Seperate the words by any non-whitespace character
  def separatewords(self,text):
    splitter=re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if s!='']


  # 如果url已经建立过索引，则返回true
  # Return true if this url is already indexed
  def isindexed(self,url):
    return False

  # 添加一个关联两个网页的链接
  # Add a link between two pages
  def addlinkref(self,urlFrom,urlTo,linkText):
    words=self.separateWords(linkText)
    fromid=self.getentryid('urllist','url',urlFrom)
    toid=self.getentryid('urllist','url',urlTo)
    if fromid==toid: return
    cur=self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
    linkid=cur.lastrowid
    for word in words:
      if word in ignorewords: continue
      wordid=self.getentryid('wordlist','word',word)
      self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid,wordid))

  # 从一小组网页开始进行广度优先搜索，直至某一给定深度，
  # 期间为网页建立索引
  # 使用广度优先算法而不是递归 易于后续修改
  # 并可以持续进行搜索，将未索引的网页列表保存，以备用
  # 并避免栈溢出
  # Starting with a list of pages, do a breadth
  # first search to the given depth, indexing pages
  # as we go
  def crawl(self,pages,depth=2):
    for i in range(depth):
      newpages={}
      #print pages
      for page in pages:
        #print page
        try:
          c=urllib2.urlopen(page)
          #print c
        except:
          print "Could not open %s" % page
          continue
        try:
          soup=BeautifulSoup(c.read())
          #print soup
          self.addtoindex(page,soup)

          # 提取网页上的链接
          links=soup('a')
          #print links
          for link in links:
            if ('href' in dict(link.attrs)):
              url=urljoin(page,link['href'])
              if url.find("'")!=-1: continue
              url=url.split('#')[0]  # remove location portion去掉位置部分
              if url[0:4]=='http' and not self.isindexed(url):
                newpages[url]=1
              #print link
              linkText=self.gettextonly(link)
              print linkText
              self.addlinkref(page,url,linkText)

          self.dbcommit()
        except:
          print "Could not parse page %s" % page

      #将新发现的链接加入pages并继续循环直到深度为depth层
      pages=newpages


  # 创建数据库并建立索引以加快搜索速度
  # Create the database tables
  def createindextables(self):
    self.con.execute('create table urllist(url)')
    self.con.execute('create table wordlist(word)')
    self.con.execute('create table wordlocation(urlid,wordid,location)')
    self.con.execute('create table link(fromid integer,toid integer)')
    self.con.execute('create table linkwords(wordid,linkid)')
    self.con.execute('create index wordidx on wordlist(word)')
    self.con.execute('create index urlidx on urllist(url)')
    self.con.execute('create index wordurlidx on wordlocation(wordid)')
    self.con.execute('create index urltoidx on link(toid)')
    self.con.execute('create index urlfromidx on link(fromid)')
    self.dbcommit()

  # PageRank计算函数 提前计算 需更新时再运行
  def calculatepagerank(self,iterations=20):
    # 清除当前的PageRank表
    # clear out the current page rank tables
    self.con.execute('drop table if exists pagerank')
    self.con.execute('create table pagerank(urlid primary key,score)')

    # 初始化每个url 令其PageRank值为1
    # initialize every url with a page rank of 1
    for (urlid,) in self.con.execute('select rowid from urllist'):
      self.con.execute('insert into pagerank(urlid,score) values (%d,1.0)' % urlid)
    self.dbcommit()

    for i in range(iterations):
      print "Iteration %d" % (i)
      for (urlid,) in self.con.execute('select rowid from urllist'):
        pr=0.15

        # 循环遍历指向当前网页的所有其他网页
        # Loop through all the pages that link to this one
        for (linker,) in self.con.execute(
        'select distinct fromid from link where toid=%d' % urlid):
          # 得到链接源对应网页的PageRank值
          # Get the page rank of the linker
          linkingpr=self.con.execute(
          'select score from pagerank where urlid=%d' % linker).fetchone()[0]

          # 根据链接源 求得总的链接数
          # Get the total number of links from the linker
          linkingcount=self.con.execute(
          'select count(*) from link where fromid=%d' % linker).fetchone()[0]
          pr+=0.85*(linkingpr/linkingcount)
        self.con.execute(
        'update pagerank set score=%f where urlid=%d' % (pr,urlid))
      self.dbcommit()

# 搜索类
class searcher:
  def __init__(self,dbname):
    self.con=sqlite.connect(dbname)

  def __del__(self):
    self.con.close()

  # 接受查询字符串作为参数 并将其拆分为多个单词
  # 并构造SQL查询 只查找包含所有不同单词的URL
  def getmatchrows(self,q):
    # 构造查询的字符串
    # Strings to build the query
    fieldlist='w0.urlid'
    tablelist=''
    clauselist=''
    wordids=[]

    # 根据空格拆分单词
    # Split the words by spaces
    words=q.split(' ')
    tablenumber=0

    for word in words:
      # 获取单词ID
      # Get the word ID
      wordrow=self.con.execute(
      "select rowid from wordlist where word='%s'" % word).fetchone()
      if wordrow!=None:
        wordid=wordrow[0]
        wordids.append(wordid)
        if tablenumber>0:
          tablelist+=','
          clauselist+=' and '
          clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
        fieldlist+=',w%d.location' % tablenumber
        tablelist+='wordlocation w%d' % tablenumber
        clauselist+='w%d.wordid=%d' % (tablenumber,wordid)
        tablenumber+=1

    # 根据各个组分 建立查询
    # Create the query from the separate parts
    fullquery='select %s from %s where %s' % (fieldlist,tablelist,clauselist)
    print fullquery
    cur=self.con.execute(fullquery)
    rows=[row for row in cur]

    return rows,wordids

  # 接受查询请求 将获取到的行集置于字典中 并以格式化列表显示
  def getscoredlist(self,rows,wordids):
    totalscores=dict([(row[0],0) for row in rows])

    # 评价函数
    # This is where we'll put our scoring functions
    weights=[(1.0,self.locationscore(rows)),
             (1.0,self.frequencyscore(rows)),
             (1.0,self.pagerankscore(rows)),
             (1.0,self.linktextscore(rows,wordids)),
             (5.0,self.nnscore(rows,wordids))]
    for (weight,scores) in weights:
      for url in totalscores:
        totalscores[url]+=weight*scores[url]

    return totalscores

  def geturlname(self,id):
    return self.con.execute(
    "select url from urllist where rowid=%d" % id).fetchone()[0]

  def query(self,q):
    rows,wordids=self.getmatchrows(q)
    scores=self.getscoredlist(rows,wordids)
    rankedscores=[(score,url) for (url,score) in scores.items()]
    rankedscores.sort()
    rankedscores.reverse()
    for (score,urlid) in rankedscores[0:10]:
      print '%f\t%s' % (score,self.geturlname(urlid))
    return wordids,[r[1] for r in rankedscores[0:10]]

  # 归一化函数 返回URL ID与数字评价值 0-1 1为最佳结果
  def normalizescores(self,scores,smallIsBetter=0):
    vsmall=0.00001 # Avoid division by zero errors
    if smallIsBetter:
      minscore=min(scores.values())
      return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
    else:
      maxscore=max(scores.values())
      if maxscore==0: maxscore=vsmall
      return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

  # 频度评价算法
  def frequencyscore(self,rows):
    counts=dict([(row[0],0) for row in rows])
    for row in rows: counts[row[0]]+=1
    return self.normalizescores(counts)

  # 文档位置评价算法
  def locationscore(self,rows):
    locations=dict([(row[0],1000000) for row in rows])
    for row in rows:
      loc=sum(row[1:])
      if loc<locations[row[0]]: locations[row[0]]=loc

    return self.normalizescores(locations,smallIsBetter=1)

  # 单词距离评价算法
  def distancescore(self,rows):
    # If there's only one word, everyone wins!
    if len(rows[0])<=2: return dict([(row[0],1.0) for row in rows])

    # Initialize the dictionary with large values
    mindistance=dict([(row[0],1000000) for row in rows])

    for row in rows:
      dist=sum([abs(row[i]-row[i-1]) for i in range(2,len(row))])
      if dist<mindistance[row[0]]: mindistance[row[0]]=dist
    return self.normalizescores(mindistance,smallIsBetter=1)

  # 外部回指链接评价算法
  def inboundlinkscore(self,rows):
    uniqueurls=dict([(row[0],1) for row in rows])
    inboundcount=dict([(u,self.con.execute('select count(*) from link where toid=%d' % u).fetchone()[0]) for u in uniqueurls])
    return self.normalizescores(inboundcount)

  # 链接文本评价算法
  def linktextscore(self,rows,wordids):
    linkscores=dict([(row[0],0) for row in rows])
    for wordid in wordids:
      cur=self.con.execute('select link.fromid,link.toid from linkwords,link where wordid=%d and linkwords.linkid=link.rowid' % wordid)
      for (fromid,toid) in cur:
        if toid in linkscores:
          pr=self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
          linkscores[toid]+=pr
    maxscore=max(linkscores.values())
    normalizedscores=dict([(u,float(l)/maxscore) for (u,l) in linkscores.items()])
    return normalizedscores

  # 从数据库中提取PageRank值并做归一化
  def pagerankscore(self,rows):
    pageranks=dict([(row[0],self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
    maxrank=max(pageranks.values())
    normalizedscores=dict([(u,float(l)/maxrank) for (u,l) in pageranks.items()])
    return normalizedscores

  def nnscore(self,rows,wordids):
    # Get unique URL IDs as an ordered list
    urlids=[urlid for urlid in dict([(row[0],1) for row in rows])]
    nnres=mynet.getresult(wordids,urlids)
    scores=dict([(urlids[i],nnres[i]) for i in range(len(urlids))])
    return self.normalizescores(scores)
