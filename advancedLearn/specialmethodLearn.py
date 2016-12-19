#-*- coding: utf-8 -*-

class Person(object):

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

class Student(Person):

    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score

    def __str__(self):
        return '(Student: %s, %s, %s)' % (self.name, self.gender, self.score)
#    __repr__ = __str__

s = Student('Bob', 'male', 88)
print s



class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return '(%s: %s)' % (self.name, self.score)

    __repr__ = __str__

    def __cmp__(self, s):
        if self.score < s.score:
            return 1
        elif self.score > s.score:
            return -1
        elif self.name < s.name:
            return -1
        elif self.name > s.name:
            return 1
        else:
            return 0

"""
    def __cmp__(self, s):
            if self.score == s.score:
                return cmp(self.name, s.name)
            return -cmp(self.score, s.score)
"""

L = [Student('Tim', 99), Student('Bob', 88), Student('Alice', 99)]
print sorted(L)

#斐波那契数列
class Fib(object):

    def __init__(self, num):
        listnum = []
        a = 0
        #lnum = 0
        b = 1
        #sumnum = 1

        for i in range(num):
            #listnum.append(lnum)
            listnum.append(a)
            #sumnum = sunnum + lnum

            #lnum = sumnum
            t = a
            a = b
            b = t + b
            #a, b = b, a + b

            self.number = listnum

    def __str__(self):
        return str(self.number)

    __repr__ = __str__

    def __len__(self):
        return len(self.number)

f = Fib(10)
print f
print len(f)

#有理数

#最大公因数解法：辗转相除法，递归实现
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

"""
def gcd(a,b):
    while b:
        a,b=b,a%b
    return a
"""


class Rational(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def __add__(self, r):
        return Rational(self.p * r.q + self.q * r.p, self.q * r.q)

    def __sub__(self, r):
        return Rational(self.p * r.q - self.q * r.p, self.q * r.q)

    def __mul__(self, r):
        return Rational(self.p * r.p, self.q * r.q)

    def __div__(self, r):
        return Rational(self.p * r.q, self.q * r.p)

    def __int__(self):
        return self.p // self.q

    def __float__(self):
        return float(self.p) / float(self.q)

    def __str__(self):
        g = gcd(self.p, self.q)
        return '%s/%s' % (self.p / g, self.q / g)

    __repr__ = __str__

r1 = Rational(1, 2)
r2 = Rational(1, 4)
print r1 + r2
print r1 - r2
print r1 * r2
print r1 / r2

print int(Rational(7, 2))
print int(Rational(1, 3))
print float(Rational(7, 2))
print float(Rational(1, 3))


#使用@将方法“伪装”成属性
class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.__score = score
        self.__grade

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self.__score = score

    @property
    def grade(self):
        return self.__grade

    @grade.setter
    def grade(self, score):
        if score  >= 80:
            self.__grade = A
        elif score < 60:
            self.__grade = C
        else:
            self.__grade = B

"""
    @property
    def grade(self):
        if self.score < 60:
            return 'C'
        if self.score < 80:
            return 'B'
        return 'A'
"""

s = Student('Bob', 59)
print s.grade

s.score = 60
print s.grade

s.score = 99
print s.grade

#使用__slot__锁定属性列表
class Person(object):

    __slots__ = ('name', 'gender')

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

class Student(Person):

    __slots__ = ('score',)

    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score

s = Student('Bob', 'male', 59)
s.name = 'Tim'
s.score = 99
print s.score