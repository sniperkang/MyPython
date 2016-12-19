#-*- coding: utf-8 -*-
#多个例子的练习代码
import math
import time
import functools

def add(x, y, f):
    return f(x) + f(y)

print add(25, 9, math.sqrt)

def cmp_ignore_case(s1, s2):
    x = s1.lower()
    y = s2.lower()
    return cmp(x, y)

print sorted(['bob', 'about', 'Zoo', 'Credit'], cmp_ignore_case)


def log(f):
    def fn(*args, **kw):
        print 'call ' + f.__name__ + '()...'
        return f(*args, **kw)
    return fn

@log
def calc_prod(lst):
    def prod(x, y):
        return x * y
    def f():
        return reduce(prod, lst)
    return f

f = calc_prod([1, 2, 3, 4])
print f()


def performance(f):
    def fn(*args, **kwargs):
        t1 = time.time()
        r = f(*args, **kwargs)
        t2 = time.time()
        print 'call %s() in %fs' % (f.__name__, (t2 - t1))
        return r
    return fn

@performance
def factorial(n):
    return reduce(lambda x,y: x*y, range(1, n+1))

print factorial(10)


def performance(unit):
    def performance_decorator(f):
        def fn(*args, **kwargs):
            t1 = time.time()
            r = f(*args, **kwargs)
            t2 = time.time()
            t = (t2 - t1) * 1000 if unit=='ms' else (t2 - t1)
            print 'call %s() in %f %s' % (f.__name__, t, unit)
            return r
        return fn
    return performance_decorator

@performance('ms')
def factorial(n):
    return reduce(lambda x,y: x*y, range(1, n+1))

print factorial(10)

def performance(unit):
    def performance_decorator(f):
        @functools.wraps(f)
        def fn(*args, **kwargs):
            t1 = time.time()
            r = f(*args, **kwargs)
            t2 = time.time()
            t = (t2 - t1) * 1000 if unit=='ms' else (t2 - t1)
            print 'call %s() in %f %s' % (f.__name__, t, unit)
            return r
        return fn
    return performance_decorator

@performance('ms')
def factorial(n):
    return reduce(lambda x,y: x*y, range(1, n+1))

print factorial.__name__


import functools

sorted_ignore_case = functools.partial(sorted, key=str.lower)

print sorted_ignore_case(['bob', 'about', 'Zoo', 'Credit'])
