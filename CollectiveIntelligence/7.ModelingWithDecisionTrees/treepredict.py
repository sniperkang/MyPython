# -*- coding: utf-8 -*-

my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

class decisionnode:
  def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
    self.col=col
    self.value=value
    self.results=results
    self.tb=tb
    self.fb=fb

# 在某一列上对数据集合进行拆分，能够处理数值型数据或名词性数据
# Divides a set on a specific column. Can handle numeric
# or nominal values
def divideset(rows,column,value):
   # 定义一个函数，令其告诉我们数据行属于第一组（返回值为true）
   # 还是第二组（返回值为false）
   # Make a function that tells us if a row is in 
   # the first group (true) or the second group (false)
   split_function=None
   if isinstance(value,int) or isinstance(value,float):
      split_function=lambda row:row[column]>=value
   else:
      split_function=lambda row:row[column]==value

   # 将数据集拆分成两个集合，并返回
   # Divide the rows into two sets and return them
   set1=[row for row in rows if split_function(row)]
   set2=[row for row in rows if not split_function(row)]
   return (set1,set2)


# 对各种可能的结果进行计数（每一行数据的最后一列记录了这一计数结果）
# Create counts of possible results (the last column of 
# each row is the result)
def uniquecounts(rows):
   results={}
   for row in rows:
      # 计数结果在最后一列
      # The result is the last column
      r=row[len(row)-1]
      #print r
      if r not in results: results[r]=0
      results[r]+=1
      #print results
   return results

# 随机放置的数据项出现于错误分类中的概率
# 值越高 说明拆分越不理想
# Probability that a randomly placed item will
# be in the wrong category
def giniimpurity(rows):
  total=len(rows)
  #print total
  counts=uniquecounts(rows)
  #print counts
  imp=0
  for k1 in counts:
    #print k1
    p1=float(counts[k1])/total
    for k2 in counts:
      if k1==k2: continue
      p2=float(counts[k2])/total
      imp+=p1*p2
  return imp

# 熵是遍历所有可能的结果之后所得到的p(x)log(p(x))之和
# 熵越高越混乱
# Entropy is the sum of p(x)log(p(x)) across all 
# the different possible results
def entropy(rows):
   from math import log
   log2=lambda x:log(x)/log(2)  
   results=uniquecounts(rows)
   #print results
   # 此处开始计算熵的值
   # Now calculate the entropy
   ent=0.0
   for r in results.keys():
      #print r
      p=float(results[r])/len(rows)
      ent=ent-p*log2(p)
   return ent



# 纯文本方式显示树 递归实现
def printtree(tree,indent=''):
   # 这是一个叶节点吗？
   # Is this a leaf node?
   if tree.results!=None:
      print str(tree.results)
   else:
      # 打印判断条件
      # Print the criteria
      print str(tree.col)+':'+str(tree.value)+'? '

      # 打印分支
      # Print the branches
      print indent+'T->',
      printtree(tree.tb,indent+'  ')
      print indent+'F->',
      printtree(tree.fb,indent+'  ')


def getwidth(tree):
  if tree.tb==None and tree.fb==None: return 1
  return getwidth(tree.tb)+getwidth(tree.fb)

def getdepth(tree):
  if tree.tb==None and tree.fb==None: return 0
  return max(getdepth(tree.tb),getdepth(tree.fb))+1


from PIL import Image,ImageDraw

def drawtree(tree,jpeg='tree.jpg'):
  w=getwidth(tree)*100
  h=getdepth(tree)*100+120

  img=Image.new('RGB',(w,h),(255,255,255))
  draw=ImageDraw.Draw(img)

  drawnode(draw,tree,w/2,20)
  img.save(jpeg,'JPEG')
  
def drawnode(draw,tree,x,y):
  if tree.results==None:
    # Get the width of each branch
    w1=getwidth(tree.fb)*100
    w2=getwidth(tree.tb)*100

    # Determine the total space required by this node
    left=x-(w1+w2)/2
    right=x+(w1+w2)/2

    # Draw the condition string
    draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))

    # Draw links to the branches
    draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
    draw.line((x,y,right-w2/2,y+100),fill=(255,0,0))
    
    # Draw the branch nodes
    drawnode(draw,tree.fb,left+w1/2,y+100)
    drawnode(draw,tree.tb,right-w2/2,y+100)
  else:
    txt=' \n'.join(['%s:%d'%v for v in tree.results.items()])
    draw.text((x-20,y),txt,(0,0,0))


def classify(observation,tree):
  if tree.results!=None:
    return tree.results
  else:
    v=observation[tree.col]
    branch=None
    if isinstance(v,int) or isinstance(v,float):
      if v>=tree.value: branch=tree.tb
      else: branch=tree.fb
    else:
      if v==tree.value: branch=tree.tb
      else: branch=tree.fb
    return classify(observation,branch)

def prune(tree,mingain):
  # If the branches aren't leaves, then prune them
  if tree.tb.results==None:
    prune(tree.tb,mingain)
  if tree.fb.results==None:
    prune(tree.fb,mingain)
    
  # If both the subbranches are now leaves, see if they
  # should merged
  if tree.tb.results!=None and tree.fb.results!=None:
    # Build a combined dataset
    tb,fb=[],[]
    for v,c in tree.tb.results.items():
      tb+=[[v]]*c
    for v,c in tree.fb.results.items():
      fb+=[[v]]*c
    
    # Test the reduction in entropy
    delta=entropy(tb+fb)-(entropy(tb)+entropy(fb)/2)

    if delta<mingain:
      # Merge the branches
      tree.tb,tree.fb=None,None
      tree.results=uniquecounts(tb+fb)

def mdclassify(observation,tree):
  if tree.results!=None:
    return tree.results
  else:
    v=observation[tree.col]
    if v==None:
      tr,fr=mdclassify(observation,tree.tb),mdclassify(observation,tree.fb)
      tcount=sum(tr.values())
      fcount=sum(fr.values())
      tw=float(tcount)/(tcount+fcount)
      fw=float(fcount)/(tcount+fcount)
      result={}
      for k,v in tr.items(): result[k]=v*tw
      for k,v in fr.items(): result[k]=v*fw      
      return result
    else:
      if isinstance(v,int) or isinstance(v,float):
        if v>=tree.value: branch=tree.tb
        else: branch=tree.fb
      else:
        if v==tree.value: branch=tree.tb
        else: branch=tree.fb
      return mdclassify(observation,branch)

def variance(rows):
  if len(rows)==0: return 0
  data=[float(row[len(row)-1]) for row in rows]
  mean=sum(data)/len(data)
  variance=sum([(d-mean)**2 for d in data])/len(data)
  return variance

# 为当前数据集选择最合适的拆分条件来构造决策树
def buildtree(rows,scoref=entropy):
  if len(rows)==0: return decisionnode()
  current_score=scoref(rows)

  # 定义一些变量以记录最佳拆分条件
  # Set up some variables to track the best criteria
  best_gain=0.0
  best_criteria=None
  best_sets=None

  # 列数
  column_count=len(rows[0])-1
  #print column_count
  for col in range(0,column_count):
    # 在当前列中生成一个由不同值构成的序列
    # Generate the list of different values in
    # this column
    column_values={}
    # 对每一行遍历第1-4列（第五列为结果）
    # 形成以不重复元素为key的dict
    for row in rows:
       #print col
       #print row
       column_values[row[col]]=1
       #print column_values
    # 接下来根据这一列中的每个值，尝试对数据集进行拆分
    # 并计算增益 以评估
    # Now try dividing the rows up for each value
    # in this column
    for value in column_values.keys():
      (set1,set2)=divideset(rows,col,value)

      # 信息增益
      # Information gain
      # p为子集及熵的权重
      p=float(len(set1))/len(rows)
      # 求当前熵与两个新群组加权平均熵的差值 即信息增益
      gain=current_score- p*scoref(set1) - (1-p)*scoref(set2)
      # 新的信息增益大于当前最优增益 意味着新群组加权平均熵较小 即更优
      if gain>best_gain and len(set1)>0 and len(set2)>0:
        best_gain=gain
        # col为遍历到的当前列 value为data中的当前列、当前行的元素
        best_criteria=(col,value)
        best_sets=(set1,set2)
  # 创建子分支
  # Create the sub branches
  # 只有到新产生群组加权平均熵大于前一次熵时
  # 即新群组更混乱时 分支才终止 此时best_gain <= 0
  # 新群组混乱度低时 继续创建子分支
  if best_gain>0:
    trueBranch=buildtree(best_sets[0])
    falseBranch=buildtree(best_sets[1])
    return decisionnode(col=best_criteria[0],value=best_criteria[1],
                        tb=trueBranch,fb=falseBranch)
  # 新群组混乱度高时 终止创建子分支
  # 当前rows已为最低级节点 即叶节点
  # 生成以叶节点为
  else:
    #print uniquecounts(rows)
    return decisionnode(results=uniquecounts(rows))
