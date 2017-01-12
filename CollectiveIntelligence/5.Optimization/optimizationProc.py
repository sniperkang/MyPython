# -*- coding: utf-8 -*-

import optimization

#s = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
#s = [4, 8, 5, 7, 6, 3, 1, 6, 1, 6, 1, 6]
#optimization.printschedule(s)
#print optimization.schedulecost(s)
domin = [(0, 9)] * (len(optimization.people) * 2)
#print len(optimization.people)
#print domin
#s = optimization.randomoptimize(domin, optimization.schedulecost)
s = optimization.hillclimb(domin, optimization.schedulecost)
#print s
print optimization.schedulecost(s)
optimization.printschedule(s)