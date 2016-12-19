#-*- coding: utf-8 -*-

class Person(object):
    pass

xiaoming = Person()
xiaohong = Person()

print xiaoming
print xiaohong
print xiaoming == xiaohong


p1 = Person()
p1.name = 'Bart'

p2 = Person()
p2.name = 'Adam'

p3 = Person()
p3.name = 'Lisa'

L1 = [p1, p2, p3]
L2 = sorted(L1, lambda p1, p2: cmp(p1.name, p2.name))

print L2[0].name
print L2[1].name
print L2[2].name

"""
除了可以直接使用self.name = 'xxx'设置一个属性外，还可以通过 setattr(self, 'name', 'xxx') 设置属性
*args 以元组的形式接受剩余非关键字参数 **kw 以字典的形式接受剩余关键字参数
.iteritems方法将字典所有的项按（key,value）的形式返回迭代器对象
"""
class Person(object):
    def __init__(self,name, gender, birth, *args, **kwargs):
        self.name = name
        self.gender = gender
        self.birth = birth
        for i in args:
            self.args[i] = args[i]
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
#        self.__dict__.update(kw)

xiaoming = Person('Xiao Ming', 'Male', '1990-1-1', job='Student')

print xiaoming.name
print xiaoming.job


class Person(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
#        self.__score = score

p = Person('Bob', 59)

print p.name
#print p.__score

#类属性
class Person(object):
    count = 0
    def __init__(self, name):
        self.name = name
        Person.count = Person.count + 1

p1 = Person('Bob')
print Person.count

p2 = Person('Alice')
print Person.count

p3 = Person('Tim')
print Person.count

class Person(object):
    __count = 0
    def __init__(self, name):
        Person.__count = Person.__count + 1
        self.name = name
        print Person.__count

p1 = Person('Bob')
p2 = Person('Alice')

#print Person.__count



class Person(object):

    def __init__(self, name, score):
        self.name = name
        self.__score = score

    def get_grade(self):
        if self.__score >= 90:
            return 'A-优秀'
        elif self.__score >= 60 and self.__score < 90:
            return 'B-及格'
        else:
            return 'C-不及格'

p1 = Person('Bob', 90)
p2 = Person('Alice', 65)
p3 = Person('Tim', 48)

print p1.get_grade()
print p2.get_grade()
print p3.get_grade()

"""
lambda: 'A'等价于return'A',相当于一个函数f，那么f()='A'.因此，p1.get_grade=f，p1.get_grade（）=f()
就是这个意思，但没有说全
p1.get_grade是属性，只不过这里的属性是一个函数对象，即f
p1.get_grade()是方法，前面的p1就是调用这个方法的对象，即实例，整句来说就是实例方法
"""
class Person(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.get_grade = lambda: 'A'

p1 = Person('Bob', 90)
print p1.get_grade
print p1.get_grade()


class Person(object):

    __count = 0

    @classmethod
    def how_many(cls):
        return cls.__count

    def __init__(self, name):
        self.name = name
        Person.__count = Person.__count + 1


print Person.how_many()

p1 = Person('Bob')

print Person.how_many()