#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
http://code.activestate.com/recipes/131499-observer-pattern/

*TL;DR
Maintains a list of dependents and notifies them of any state changes.

行为模式--观察者模式(理解观察者这个意思, 敌不动我不动)
观察者模式: 当对象之间存在一对多关系时, 一个对象被修改时, 自动的通知它的依赖对象.
主要解决: 一个对象状态改变给其他对象通知的问题，而且要考虑到易用和低耦合，保证高度的协作
应用场景:
    拍卖的时候，拍卖师观察最高标价，然后通知给其他竞价者竞价; 使用观察者模式创建一种链式触发机制
    抽象模型有两个方面，一个方面依赖于另一个方面。将这些方面封装在独立的对象中使它们可以各自独立地改变和复用

*Examples in Python ecosystem:
Django Signals: https://docs.djangoproject.com/en/2.1/topics/signals/
Flask Signals: http://flask.pocoo.org/docs/1.0/signals/
"""

from __future__ import print_function


class Subject(object):
    """ 观察者管理对象 """
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """ 放入待观察链中 """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """ 从待观察链中删除 """
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)


# Example usage
class Data(Subject):
    """ 观察者(观察者管理对象子类) """
    def __init__(self, name=''):
        Subject.__init__(self)
        self.name = name
        self._data = 0

    # 利用装饰器property来进行属性访问(__get__)
    @property
    def data(self):
        return self._data

    # __set__, 每一次设置都会通知
    @data.setter
    def data(self, value):
        self._data = value
        # 一般都是被依赖对象发起通知消息
        self.notify()


class HexViewer:
    def update(self, subject):
        print(u'HexViewer: Subject %s has data 0x%x' % (subject.name, subject.data))


class DecimalViewer:
    def update(self, subject):
        print(u'DecimalViewer: Subject %s has data %d' % (subject.name, subject.data))


# Example usage...
def main():
    """
    >>> data1 = Data('Data 1')
    >>> data2 = Data('Data 2')
    >>> view1 = DecimalViewer()
    >>> view2 = HexViewer()
    >>> data1.attach(view1)
    >>> data1.attach(view2)
    >>> data2.attach(view2)
    >>> data2.attach(view1)

    >>> data1.data = 10
    DecimalViewer: Subject Data 1 has data 10
    HexViewer: Subject Data 1 has data 0xa

    >>> data2.data = 15
    HexViewer: Subject Data 2 has data 0xf
    DecimalViewer: Subject Data 2 has data 15

    >>> data1.data = 3
    DecimalViewer: Subject Data 1 has data 3
    HexViewer: Subject Data 1 has data 0x3

    >>> data2.data = 5
    HexViewer: Subject Data 2 has data 0x5
    DecimalViewer: Subject Data 2 has data 5

    # Detach HexViewer from data1 and data2
    >>> data1.detach(view2)
    >>> data2.detach(view2)

    >>> data1.data = 10
    DecimalViewer: Subject Data 1 has data 10

    >>> data2.data = 15
    DecimalViewer: Subject Data 2 has data 15
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
