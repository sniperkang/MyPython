# -*- coding: utf-8 -*-

import time
import random
import math

people = [('Seymour','BOS'),
          ('Franny','DAL'),
          ('Zooey','CAK'),
          ('Walt','MIA'),
          ('Buddy','ORD'),
          ('Les','OMA')]
# Laguardia
# New York的LaGuardia机场
destination='LGA'

flights={}
# 
for line in file('schedule.txt'):
  origin,dest,depart,arrive,price=line.strip().split(',')
  #print origin,dest,depart,arrive,price
  flights.setdefault((origin,dest),[])

  # Add details to the list of possible flights
  # 将航班详情添加到航班列表中
  flights[(origin,dest)].append((depart,arrive,int(price)))
#print 'flight = ', flights
#print len(flights)

# 用于计算给定时间在一天中的分钟数
def getminutes(t):
  x=time.strptime(t,'%H:%M')
  return x[3]*60+x[4]

# 将人们决定搭乘的所有航班打印成表格
def printschedule(r):
  for d in range(len(r)/2):
    #print d
    name=people[d][0]
    #print name
    origin=people[d][1]
    #print origin
    #print destination
    #out=flights[(origin,destination)][int(r[d])]
    out=flights[(origin,destination)][int(r[2*d])]
    #print int(r[d])
    #print int(r[2*d])
    #print out
    #ret=flights[(destination,origin)][int(r[d+1])]
    ret=flights[(destination,origin)][int(r[2*d+1])]
    #print int(r[d+1])
    #print int(r[2*d+1])
    #print ret
    print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,
                                                  out[0],out[1],out[2],
                                                  ret[0],ret[1],ret[2])

def schedulecost(sol):
  totalprice=0
  latestarrival=0
  earliestdep=24*60

  for d in range(len(sol)/2):
    # Get the inbound and outbound flights
    # 得到往程航班和返程航班
    origin=people[d][1]
    #outbound=flights[(origin,destination)][int(sol[d])]
    #returnf=flights[(destination,origin)][int(sol[d+1])]
    """
    print d
    print 2*d+1
    print sol
    print int(sol[2*d+1])
    print flights[(origin,destination)]
    print flights[(origin,destination)][int(sol[2*d])]
    print flights[(destination,origin)]
    print flights[(destination,origin)][int(sol[2*d+1])]
    """
    outbound=flights[(origin,destination)][int(sol[2*d])]
    returnf=flights[(destination,origin)][int(sol[2*d+1])]
    #print outbound
    #print returnf
    
    # Total price is the price of all outbound and return flights
    # 总价格等于所有往程航班和返程航班价格之和
    totalprice+=outbound[2]
    totalprice+=returnf[2]
    
    # Track the latest arrival and earliest departure
    # 记录最晚到达时间和最早离开时间
    if latestarrival<getminutes(outbound[1]): latestarrival=getminutes(outbound[1])
    if earliestdep>getminutes(returnf[0]): earliestdep=getminutes(returnf[0])
  
  # Every person must wait at the airport until the latest person arrives.
  # They also must arrive at the same time and wait for their flights.
  # 每个人必须在机场等待直到最后一个人到达为止
  # 他们也必须在相同时间到达，并等候他们的返程航班
  totalwait=0
  for d in range(len(sol)/2):
    origin=people[d][1]
    #outbound=flights[(origin,destination)][int(sol[d])]
    #returnf=flights[(destination,origin)][int(sol[d+1])]
    outbound=flights[(origin,destination)][int(sol[2*d])]
    returnf=flights[(destination,origin)][int(sol[2*d+1])]
    totalwait+=latestarrival-getminutes(outbound[1])
    totalwait+=getminutes(returnf[0])-earliestdep  

  # Does this solution require an extra day of car rental? That'll be $50!
  # 这个题解要求多付一天的租车费用吗？如果是，则费用为50美元
  if latestarrival<earliestdep: totalprice+=50
  
  return totalprice+totalwait

def randomoptimize(domain,costf):
  best=999999999
  bestr=None
  for i in range(0,1000):
    # 创建一个随机解
    # Create a random solution
    r=[float(random.randint(domain[i][0],domain[i][1])) 
       for i in range(len(domain))]
    #print r

    # 得到成本
    # Get the cost
    cost=costf(r)
    #print cost, best

    #与到目前为止的最优解进行比较
    # Compare it to the best one so far
    if cost<best:
      best=cost
      bestr=r
    #print best
    #print bestr
  return bestr

# 爬山法
def hillclimb(domain,costf):
  # Create a random solution
  # 创建一个随机解
  sol=[random.randint(domain[i][0],domain[i][1])
      for i in range(len(domain))]
  # Main loop
  # 主循环
  while 1:
    # Create list of neighboring solutions
    # 创建相邻解的列表
    neighbors=[]
    
    for j in range(len(domain)):
      # One away in each direction
      # 在每个方向上相对于原值偏离一点
      if sol[j]>domain[j][0]:
        neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
      if sol[j]<domain[j][1]:
        neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])

    # See what the best solution amongst the neighbors is
    # 在相邻解中寻找最优解
    current=costf(sol)
    best=current
    for j in range(len(neighbors)):
      cost=costf(neighbors[j])
      if cost<best:
        best=cost
        sol=neighbors[j]

    # If there's no improvement, then we've reached the top
    # 如果没有更好的解，则退出循环
    if best==current:
      break
  return sol

def annealingoptimize(domain,costf,T=10000.0,cool=0.95,step=1):
  # Initialize the values randomly
  vec=[float(random.randint(domain[i][0],domain[i][1])) 
       for i in range(len(domain))]
  
  while T>0.1:
    # Choose one of the indices
    i=random.randint(0,len(domain)-1)

    # Choose a direction to change it
    dir=random.randint(-step,step)

    # Create a new list with one of the values changed
    vecb=vec[:]
    vecb[i]+=dir
    if vecb[i]<domain[i][0]: vecb[i]=domain[i][0]
    elif vecb[i]>domain[i][1]: vecb[i]=domain[i][1]

    # Calculate the current cost and the new cost
    ea=costf(vec)
    eb=costf(vecb)
    p=pow(math.e,(-eb-ea)/T)

    # Is it better, or does it make the probability
    # cutoff?
    if (eb<ea or random.random()<p):
      vec=vecb      

    # Decrease the temperature
    T=T*cool
  return vec

def geneticoptimize(domain,costf,popsize=50,step=1,
                    mutprob=0.2,elite=0.2,maxiter=100):
  # Mutation Operation
  def mutate(vec):
    i=random.randint(0,len(domain)-1)
    if random.random()<0.5 and vec[i]>domain[i][0]:
      return vec[0:i]+[vec[i]-step]+vec[i+1:] 
    elif vec[i]<domain[i][1]:
      return vec[0:i]+[vec[i]+step]+vec[i+1:]
  
  # Crossover Operation
  def crossover(r1,r2):
    i=random.randint(1,len(domain)-2)
    return r1[0:i]+r2[i:]

  # Build the initial population
  pop=[]
  for i in range(popsize):
    vec=[random.randint(domain[i][0],domain[i][1]) 
         for i in range(len(domain))]
    pop.append(vec)
  
  # How many winners from each generation?
  topelite=int(elite*popsize)
  
  # Main loop 
  for i in range(maxiter):
    scores=[(costf(v),v) for v in pop]
    scores.sort()
    ranked=[v for (s,v) in scores]
    
    # Start with the pure winners
    pop=ranked[0:topelite]
    
    # Add mutated and bred forms of the winners
    while len(pop)<popsize:
      if random.random()<mutprob:

        # Mutation
        c=random.randint(0,topelite)
        pop.append(mutate(ranked[c]))
      else:
      
        # Crossover
        c1=random.randint(0,topelite)
        c2=random.randint(0,topelite)
        pop.append(crossover(ranked[c1],ranked[c2]))
    
    # Print current best score
    print scores[0][0]
    
  return scores[0][1]
