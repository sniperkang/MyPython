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