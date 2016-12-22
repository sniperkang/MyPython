#-*- coding: utf-8 -*-

import feedparser
import re

# 返回一个RSS订阅源的标题和包含单词计数情况的字典
# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
  # 解析订阅源
  # Parse the feed
  d=feedparser.parse(url)
  #print d
  wc={}

  # 循环遍历所有的文章条目
  # Loop over all the entries
  for e in d.entries:
    #print e
    if 'summary' in e: summary=e.summary
    else: summary=e.description

    # 提取一个单词列表
    # 提取一个本url的单词列表，并对单词计数
    # Extract a list of words
    words=getwords(e.title+' '+summary)
    #print words
    for word in words:
      wc.setdefault(word,0)
      wc[word]+=1
  return d.feed.title,wc

def getwords(html):
  # 去除所有HTML
  # Remove all the HTML tags
  #print html
  # 正则实现所有<...>用''替换
  txt=re.compile(r'<[^>]+>').sub('',html)
  print txt

  # 利用所有非字母字符拆分出单词
  # Split words by all non-alpha characters
  words=re.compile(r'[^A-Z^a-z]+').split(txt)
  print words

  # 转化成小写形式
  # Convert to lowercase
  return [word.lower() for word in words if word!='']

# 针对每个博客进行单词统计及出现这些单词的博客数目（apcount）
apcount={}
wordcounts={}
feedlist=[line for line in file('feedlist.txt')]
#print feedlist
for feedurl in feedlist:
  try:
    title,wc=getwordcounts(feedurl)
    wordcounts[title]=wc
    for word,count in wc.items():
      apcount.setdefault(word,0)
      if count>1:
        apcount[word]+=1
  except:
    print 'Failed to parse feed %s' % feedurl

# 将出现某单词的博客数目，除以博客总数，出现频率在10%-50%的单词放入wordlist
wordlist=[]
for w,bc in apcount.items():
  frac=float(bc)/len(feedlist)
  if frac>0.1 and frac<0.5:
    wordlist.append(w)

# 生成单词为列名，博客名为行名的矩阵，元素为单词在此博客出现次数
out=file('blogdata1.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
  #print blog
  out.write(blog)
  for word in wordlist:
    if word in wc: out.write('\t%d' % wc[word])
    else: out.write('\t0')
  out.write('\n')
