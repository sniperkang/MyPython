# -*- coding: utf-8 -*-

import random
import math

# The dorms, each of which has two available spaces
dorms=['Zeus','Athena','Hercules','Bacchus','Pluto']

# People, along with their first and second choices
prefs=[('Toby', ('Bacchus', 'Hercules')),
       ('Steve', ('Zeus', 'Pluto')),
       ('Karen', ('Athena', 'Zeus')),
       ('Sarah', ('Zeus', 'Pluto')),
       ('Dave', ('Athena', 'Bacchus')), 
       ('Jeff', ('Hercules', 'Pluto')), 
       ('Fred', ('Pluto', 'Athena')), 
       ('Suzie', ('Bacchus', 'Hercules')), 
       ('Laura', ('Bacchus', 'Hercules')), 
       ('James', ('Hercules', 'Athena'))]

# [(0,9),(0,8),(0,7),(0,6),...,(0,0)]
# 搜索的定义域
domain=[(0,(len(dorms)*2)-i-1) for i in range(0,len(dorms)*2)]
#print domain

def printsolution(vec):
  slots=[]
  # Create two slots for each dorm
  # 为每个宿舍建两个槽
  for i in range(len(dorms)):
      slots+=[i,i]
      #print slots

  # Loop over each students assignment
  # 遍历每一名学生的安置情况
  # i表示第i个学生
  for i in range(len(vec)):
    # x为第i个学生选择的插槽在剩余插槽中的位置
    x=int(vec[i])
    #print x

    # Choose the slot from the remaining ones
    # 从剩余槽中选择
    # 如果输入为全零 则总是选留下的宿舍中最靠前的
    dorm=dorms[slots[x]]
    #print dorm
    # Show the student and assigned dorm
    # 输出学生及其被分配的宿舍
    print prefs[i][0],dorm
    # Remove this slot
    # 删除该槽
    del slots[x]

# 成本函数
def dormcost(vec):
  cost=0
  # Create list a of slots
  # 建立一个槽序列
  slots=[0,0,1,1,2,2,3,3,4,4]

  # Loop over each student
  # 遍历每一名学生
  print vec
  for i in range(len(vec)):
    x=int(vec[i])
    dorm=dorms[slots[x]]
    pref=prefs[i][1]
    # First choice costs 0, second choice costs 1
    # 首选成本值为0，次选成本值为1
    if pref[0]==dorm: cost+=0
    elif pref[1]==dorm: cost+=1
    else: cost+=3
    # Not on the list costs 3
    # 不在选择之列则成本值为3

    # Remove selected slot
    # 删除选中的槽
    del slots[x]
  print cost
  return cost
