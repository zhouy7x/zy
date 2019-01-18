#!/usr/bin/python3
# -*-coding:utf-8-*-
"""
@author:lhj
@time: 2018/12/18
"""

class Index():
    def __init__(self):
        self.lock = None

    @property
    def _lock(self):
        return self.lock

    @_lock.setter
    def _lock(self, n):
        print(1111111111)
        self.lock = n

    @_lock.deleter
    def _lock(self):
        del self.lock

    @staticmethod
    def test1(foo):
        def inside(*args, **kwargs):
            return foo()
        return inside

    def test2(self):
        print("test2")


# a = Index()
# print a._lock
# a._lock = 1
# print a._lock
#
# del a._lock
# a.test2()




class Person:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        print("get name called")
        return self._name

    @name.setter
    def name(self, name):
        print("set name called")
        if not isinstance(name, str):
            raise TypeError("Expected a string")
        self._name = name

person = Person("Tom")
print(person.name)
