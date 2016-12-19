ll =[1, 2, 3, 4, 5, 6, 7, 8, 9]
print [v * 10 for v in ll if v > 4]
timesten = dict([(v, v * 10) for v in ll])
print timesten
