#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*What is this pattern about?
The Borg pattern (also known as the Monostate pattern) is a way to
implement singleton behavior, but instead of having only one instance
of a class, there are multiple instances that share the same state. In
other words, the focus is on sharing state instead of sharing instance
identity.

*What does this example do?
To understand the implementation of this pattern in Python, it is
important to know that, in Python, instance attributes are stored in a
attribute dictionary called __dict__. Usually, each instance will have
its own dictionary, but the Borg pattern modifies this so that all
instances have the same dictionary.
In this example, the __shared_state attribute will be the dictionary
shared between all instances, and this is ensured by assigining
__shared_state to the __dict__ variable when initializing a new
instance (i.e., in the __init__ method). Other attributes are usually
added to the instance's attribute dictionary, but, since the attribute
dictionary itself is shared (which is __shared_state), all other
attributes will also be shared.
For this reason, when the attribute self.state is modified using
instance rm2, the value of self.state in instance rm1 also changes. The
same happens if self.state is modified using rm3, which is an
instance from a subclass.
Notice that even though they share attributes, the instances are not
the same, as seen by their ids.


创建型模式--Borg模式
Borg模式: 利用python实现单例的一种方式.
Borg: 一个邪恶种族，所有的 Borg 成员，都随时听从一个中央命令机构，叫做 Collective (集体).
        这个集体, 随时能够和任何一个 Borg 成员通信， 在 Borg 成员里共享一切信息.

原理: 对于python的一个类而言, self.__dict__是可以重新绑定的. 如果我们在__init__方法中重新绑定一个新的字典,
        那么所有的对象就拥有"we are one"的性质

与单例模式区别: 单例模式关注的是对象的一致性, 即在单例模式中永远放回同一个对象. Borg模式和单例模式都支持
        状态的一致性. 在GC 方面单例模式的性能优于 Brog模式.


*Where is the pattern used practically?
Sharing state is useful in applications like managing database connections:
https://github.com/onetwopunch/pythonDbTemplate/blob/master/database.py

*References:
https://fkromer.github.io/python-pattern-references/design/#singleton

*TL;DR
Provides singleton-like behavior sharing state between instances.
"""


class Borg(object):
    __shared_state = {}  # 所有成员共享

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.state = 'Init'  # __dict__实际包含self.state属性

    def __str__(self):
        return self.state


class YourBorg(Borg):
    pass


if __name__ == '__main__':
    rm1 = Borg()
    rm2 = Borg()

    rm1.state = 'Idle'
    rm2.state = 'Running'

    print('rm1: {0}'.format(rm1))
    print('rm2: {0}'.format(rm2))

    rm2.state = 'Zombie'

    print('rm1: {0}'.format(rm1))
    print('rm2: {0}'.format(rm2))

    print('rm1 id: {0}'.format(id(rm1)))
    print('rm2 id: {0}'.format(id(rm2)))

    rm3 = YourBorg()

    print('rm1: {0}'.format(rm1))
    print('rm2: {0}'.format(rm2))
    print('rm3: {0}'.format(rm3))

### OUTPUT ###
# rm1: Running
# rm2: Running
# rm1: Zombie
# rm2: Zombie
# rm1 id: 140732837899224
# rm2 id: 140732837899296
# rm1: Init
# rm2: Init
# rm3: Init
