#-*- coding: utf-8 -*-
from recommendations import critics
#print critics['Lisa Rose']['Lady in the Water']

#critics['Toby']['Snakes on a Plane'] = 4.5
#print critics['Toby']

from math import sqrt
#print sqrt(pow(4.5 - 4, 2) + pow(1 - 2, 2))
#print 1/(1 + sqrt(pow(4.5 - 4, 2) + pow(1 - 2, 2)))

import recommendations
#print recommendations.sim_distance(recommendations.critics, 'Lisa Rose', 'Gene Seymour')
#print recommendations.sim_distance(recommendations.critics, 'Lisa Rose', 'Michael Phillips')

#print recommendations.sim_pearson(recommendations.critics, 'Lisa Rose', 'Gene Seymour')
#print recommendations.sim_pearson(recommendations.critics, 'Lisa Rose', 'Michael Phillips')

#print recommendations.topMatches(recommendations.critics, 'Toby', n=3)

#print recommendations.getRecommendations(recommendations.critics, 'Toby')
#print recommendations.getRecommendations(recommendations.critics, 'Toby', similarity=recommendations.sim_distance)

movies = recommendations.transformPrefs(recommendations.critics)
#print recommendations.topMatches(movies, 'Superman Returns')
#print recommendations.getRecommendations(movies, 'Just My Luck')

# 基于物品的协作性过滤
#itemsim = recommendations.calculateSimilarItems(recommendations.critics)
#print itemsim

#prefs = recommendations.loadMovieLens()
#print prefs
#print prefs['87']
# 基于用户推荐
#print recommendations.getRecommendations(prefs, '87')[0:30]
# 基于物品推荐 生成itemsim较慢
#itemsim = recommendations.calculateSimilarItems(prefs, n=50)
#print recommendations.getRecommendedItems(prefs, itemsim, '87')[0:30]

# 练习 先找出最相似的5名用户 再对这5名用户使用选定的
matchedPersons = recommendations.topMatchedPersons(critics, 'Toby')
#print matchedPersons
print recommendations.sim_tanimoto(recommendations.critics, 'Lisa Rose', 'Gene Seymour')
print recommendations.sim_tanimoto(recommendations.critics, 'Lisa Rose', 'Michael Phillips')
#print recommendations.getRecommendations1(recommendations.critics, matchedPersons, 'Toby', similarity=recommendations.sim_distance)
