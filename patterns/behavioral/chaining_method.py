#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
行为模式 -- 链式方法模式

功能: 每次调用都会返回对象本身或者其他对象
使用场景:
    1. API: 采用Chaining Method方式设计API可以使代码变得非常简洁
    2. 数据处理: Chaining Method Way可以让数据保持单项流动
@data pipeline思想:
    OOP Way: 数据从左向右流动, 例如: Processor.new([1, 2, 3]).plus(1).even().sum()
    Function programming way: 数据从右向左流动, 例如sum(even(plus(1, [1, 2, 3])))

即将一个整体大功能拆分为一个个小功能, 数据输出都是在对象内部流动, 在任意环节都可以通过非链式方法或者
变量属性返回最后结果.
"""


from __future__ import print_function


class Person(object):
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def do_action(self):
        print(self.name, self.action.name, end=' ')
        return self.action


class Action(object):
    def __init__(self, name):
        self.name = name

    def amount(self, val):
        print(val, end=' ')
        return self

    def stop(self):
        print('then stop')


def main():
    """
    >>> move = Action('move')
    >>> person = Person('Jack', move)
    >>> person.do_action().amount('5m').stop()
    Jack move 5m then stop
    """


if __name__ == '__main__':
    import doctest
    doctest.testmod()
