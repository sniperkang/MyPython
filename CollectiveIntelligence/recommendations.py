#-*- coding: utf-8 -*-
#一个涉及影评者及其对几部影片评分情况的字典
# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


from math import sqrt

# 欧几里德距离（Euclidean Distance）
# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
  # 得到shared_items列表
  # Get the list of shared_items
  si={}
  for item in prefs[person1]: 
    if item in prefs[person2]: si[item]=1

  # 如果二者没有共同之处，则返回0
  # if they have no ratings in common, return 0
  if len(si)==0: return 0

  # 计算所有差值的平方和
  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                      for item in prefs[person1] if item in prefs[person2]])

  return 1/(1+sum_of_squares)

# 皮尔逊相关系数（Pearson Correlation Coefficient）
# 返回p1和p2的皮尔逊相关系数
# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
  # 得到双方都曾评价过的物品列表
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]: 
    if item in prefs[p2]: si[item]=1

  # 如果双方没有共同之处，则返回0,1为完全相同
  # if they are no ratings in common, return 0
  if len(si)==0: return 0

  # 得到列表元素个数
  # Sum calculations
  n=len(si)

  # 所有偏好求和
  # Sums of all the preferences
  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])

  # 求平方和
  # Sums of the squares
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	

  # 求乘积之和
  # Sum of the products
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

  # 计算皮尔逊评价值
  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r

# 练习
# Tanimoto 系数（Tanimoto Coefficient）
# Returns the Pearson correlation coefficient for p1 and p2
def sim_tanimoto(prefs,p1,p2):
  # 得到双方都曾评价过的物品列表
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]:
    if item in prefs[p2]: si[item]=1

  # 如果双方没有共同之处，则返回0,1为完全相同
  # if they are no ratings in common, return 0
  if len(si)==0: return 0

  # 得到列表元素个数
  # Sum calculations
  n=len(si)

  # 求平方和
  # Sums of the squares
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

  # 求乘积之和
  # Sum of the products
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

  # 计算Tanimoto评价值
  # Calculate r (Tanimoto score)
  num=pSum
  den=sqrt(sum1Sq) + sqrt(sum2Sq) - pSum
  if den==0: return 0

  r=num/den

  return r


# 从反映偏好的字典中返回最为匹配者
# 返回结果的个数和相似度函数均为可选参数
# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
  # 对列表进行排序，评价值最高者排在最前面
  scores.sort()
  scores.reverse()
  return scores[0:n]

# 练习
# 返回前n个最为匹配者组成的list
def topMatchedPersons(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other)
                  for other in prefs if other!=person]
  # 对列表进行排序，评价值最高者排在最前面
  scores.sort()
  scores.reverse()
  matched = []
  matchedPerson = ()
  for i in range(5):
      matchedPerson = scores[i][1]
      #matched.append(matchedPerson[1])
      matched.append(matchedPerson)
  return matched[0:n]


# 利用所有他人评价值的加权平均，为某人提供建议
# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # 不要和自己做比较
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)

    # 忽略评价值为零或小于零的情况
    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:
	    
      # 只对自己还未曾看过的影片进行评价
      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item]==0:
        # 相似度*评价值
        # Similarity * Score
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        # 相似度之和
        # Sum of similarities
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # 建立一个归一化的列表
  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # 返回经过排序的列表
  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings

# 练习
# 利用n个最相似用户的评价值的加权平均，为某人提供建议
def getRecommendations1(prefs,matched,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in matched:
    # 不要和自己做比较
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)

    # 忽略评价值为零或小于零的情况
    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:

      # 只对自己还未曾看过的影片进行评价
      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item]==0:
        # 相似度*评价值
        # Similarity * Score
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        # 相似度之和
        # Sum of similarities
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # 建立一个归一化的列表
  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # 返回经过排序的列表
  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings

def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})

      # 将物品和人员对调
      # Flip item and person
      result[item][person]=prefs[person][item]
  return result


def calculateSimilarItems(prefs,n=10):
  # 建立字典，以给出与这些物品最为相近的所有其他物品
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}
  # 以物品为中心对偏好矩阵实施倒置处理
  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # 针对大数据集更新状态变量
    # Status updates for large datasets
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # 找到最为相近的物品
    # Find the most similar items to this one
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result

def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # 循环遍历由当前用户评分的物品
  # Loop over items rated by this user
  for (item,rating) in userRatings.items( ):

    # 循环遍历与当前物品相似的物品
    # Loop over items similar to this one
    for (similarity,item2) in itemMatch[item]:

      # 如果该用户已经对当前物品做过评价，则将其忽略
      # Ignore if this user has already rated this item
      if item2 in userRatings: continue
      # 评价值与相似度的加权之和
      # Weighted sum of rating times similarity
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      # 全部相似度之和
      # Sum of all the similarities
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  # 将每个合计值除以加权和，求出平均值
  # Divide each total score by total weighting to get an average
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  # 按最高值到最低值的顺序，返回评分结果
  # Return the rankings from highest to lowest
  rankings.sort( )
  rankings.reverse( )
  return rankings

#从数据构建用户评分矩阵
#def loadMovieLens(path='/data/movielens'):
def loadMovieLens(path='./ml-100k'):
  # 获取影片标题
  # Get movie titles
  movies={}
  for line in open(path+'/u.item'):
    (id,title)=line.split('|')[0:2]
    movies[id]=title

  # 加载数据
  # Load data
  prefs={}
  for line in open(path+'/u.data'):
    (user,movieid,rating,ts)=line.split('\t')
    prefs.setdefault(user,{})
    prefs[user][movies[movieid]]=float(rating)
  return prefs
