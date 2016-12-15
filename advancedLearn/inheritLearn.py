#-*- coding: utf-8 -*-
#类继承

class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

class Teacher(Person):

    def __init__(self, name, gender, course):
        super(Teacher, self).__init__(name, gender)
        self.course = course

t = Teacher('Alice', 'Female', 'English')
print t.name
print t.course


class Person(object):

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

class Student(Person):

    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score

class Teacher(Person):

    def __init__(self, name, gender, course):
        super(Teacher, self).__init__(name, gender)
        self.course = course

t = Teacher('Alice', 'Female', 'English')

print isinstance(t, Person)
print isinstance(t, Student)
print isinstance(t, Teacher)
print isinstance(t, object)


"""
动态语言的多态和静态语言c++等多态含义不太一样，
c++中的多态就是参数数量和类型不同的方法就是不同方法，
而动态语言中的多态其实值的是方法的寻找过程，
即向右找到类（或者单件类），在类中找不到的话再找父类，
一直在祖先链中找到或者找不到为止，先找到的就被调用
"""
import json

class Students(object):
    def read(self):
        return r'["Tim","Bob","Alice"]'

s = Students()

print json.load(s)


class Person(object):
    pass

class Student(Person):
    pass

class Teacher(Person):
    pass

class SkillMixin(object):
    pass

class BasketballMixin(SkillMixin):
    def skill(self):
        return 'basketball'

class FootballMixin(SkillMixin):
    def skill(self):
        return 'football'

class BStudent(BasketballMixin, Student):
#    def __init__(self, a):
#        super(BStudent, self).__init__(a)
    pass

class FTeacher(FootballMixin, Teacher):
#    def __init__(self, a):
#        super(FTeacher, self).__init__(a)
    pass

s = BStudent()
print s.skill()

t = FTeacher()
print t.skill()


class Person(object):

    def __init__(self, name, gender, **kw):
        self.name = name
        self.gender = gender
        for k, v in kw.iteritems():
            setattr(self, k, v)
#        self.__dict__.update(kw)

p = Person('Bob', 'Male', age=18, course='Python')
print p.age
print p.course