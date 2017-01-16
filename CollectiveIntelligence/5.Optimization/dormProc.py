# -*- coding: utf-8 -*-

import dorm
import optimization

#dorm.printsolution([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

#s = optimization.randomoptimize(dorm.domain, dorm.dormcost)
#print dorm.dormcost(s)
#dorm.printsolution(s)

s = optimization.geneticoptimize(dorm.domain, dorm.dormcost)
dorm.printsolution(s)



