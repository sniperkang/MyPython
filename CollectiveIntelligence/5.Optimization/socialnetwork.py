# -*- coding: utf-8 -*-

import math

people=['Charlie','Augustus','Veruca','Violet','Mike','Joe','Willy','Miranda']

links=[('Augustus', 'Willy'), 
       ('Mike', 'Joe'), 
       ('Miranda', 'Mike'), 
       ('Violet', 'Augustus'), 
       ('Miranda', 'Willy'), 
       ('Charlie', 'Mike'), 
       ('Veruca', 'Joe'), 
       ('Miranda', 'Augustus'), 
       ('Willy', 'Augustus'), 
       ('Joe', 'Charlie'), 
       ('Veruca', 'Augustus'), 
       ('Miranda', 'Joe')]


def crosscount(v):
  # Convert the number list into a dictionary of person:(x,y)
  # 将数字序列转换成一个字典
  loc=dict([(people[i],(v[i*2],v[i*2+1])) for i in range(0,len(people))])
  total=0
  
  # Loop through every pair of links
  # 遍历每一对连线 双循环倒三角形 即只向后遍历
  for i in range(len(links)):
    for j in range(i+1,len(links)):

      #print i, j
      # Get the locations
      # 获取坐标位置
      (x1,y1),(x2,y2)=loc[links[i][0]],loc[links[i][1]]
      #print links[i][0], links[i][1]
      #print x1,y1,x2,y2
      (x3,y3),(x4,y4)=loc[links[j][0]],loc[links[j][1]]
      #print links[i][0], links[i][1]
      #print x3,y3,y4,y4
      
      den=(y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)

      # den==0 if the lines are parallel
      # 如果两线平行，则den==0
      if den==0: continue

      # Otherwise ua and ub are the fraction of the
      # line where they cross
      # 否则， ua与ub就是两条交叉线的分数值
      ua=((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/den
      ub=((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/den
      
      # If the fraction is between 0 and 1 for both lines
      # then they cross each other
      # 如果两条线的分数值介于0和1之间，则两线彼此相交
      if ua>0 and ua<1 and ub>0 and ub<1:
        total+=1
    for i in range(len(people)):
      for j in range(i+1,len(people)):
        # Get the locations of the two nodes
        # 获得两结点的位置
        (x1,y1),(x2,y2)=loc[people[i]],loc[people[j]]

        # Find the distance between them
        # 计算两结点的间距
        dist=math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
        # Penalize any nodes closer than 50 pixels
        # 对间距小于50个像素的结点进行判罚
        if dist<50:
          total+=(1.0-(dist/50.0))
        
  return total
from PIL import Image,ImageDraw

def drawnetwork(sol):
  # Create the image
  # 建立image对象
  img=Image.new('RGB',(400,400),(255,255,255))
  draw=ImageDraw.Draw(img)

  # Create the position dict
  # 建立标示位置信息的字典
  pos=dict([(people[i],(sol[i*2],sol[i*2+1])) for i in range(0,len(people))])

  # 绘制连线
  for (a,b) in links:
    draw.line((pos[a],pos[b]),fill=(255,0,0))

  # 绘制代表人的结点
  for n,p in pos.items():
    draw.text(p,n,(0,0,0))

  #img.show()
  img.save('network.jpg','JPEG')


domain=[(10,370)]*(len(people)*2)