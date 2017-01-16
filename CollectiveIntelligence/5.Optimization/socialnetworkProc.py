# -*- coding: utf-8 -*-

import socialnetwork
import optimization

#sol = optimization.randomoptimize(socialnetwork.domain, socialnetwork.crosscount)
#print sol
#print socialnetwork.crosscount(sol)

sol = optimization.annealingoptimize(socialnetwork.domain, socialnetwork.crosscount, step=50, cool=0.99)
print sol
print  socialnetwork.crosscount(sol)
socialnetwork.drawnetwork(sol)