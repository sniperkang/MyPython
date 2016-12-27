import docclass

#cl = docclass.classifier(docclass.getwords)
#cl.train('the quick brown fox jumps over the lazy dog', 'good')
#cl.train('make quick money in the online casino', 'bad')
#cl.fcount('quick', 'good')
#docclass.sampletrain(cl)
#cl.fprob('quick', 'good')
#cl.weightedprob('money', 'good', cl.fprob)

#cl = docclass.naivebayes(docclass.getwords)
#docclass.sampletrain(cl)
#cl.fprob('quick rabbit', 'good')
#cl.fprob('quick rabbit', 'bad')
#cl.fprob('quick rabbit', default='unknown')
#cl.fprob('quick money', default='unknown')

#cl.setthreshold('bad', 3.0)
#cl.fprob('quick money', default='unknown')

#for i in range(10): docclass.sampletrain(cl)
#cl.classify('quick money', default='unknown')

cl = docclass.fisherclassifier(docclass.getwords)
cl.setdb('test1.db')
docclass.sampletrain(cl)
cl2 = docclass.naivebayes(docclass.getwords)
cl2.setdb('test1.db')
print cl2.classify('quick money')



