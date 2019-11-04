#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
http://code.activestate.com/recipes/413838-memento-closure/

行为模式--备忘录模式

备忘录模式: 保存一个对象的状态, 以便在适当的时候恢复对象状态.
意图: 在不破坏封装性的前提下，捕获一个对象的内部状态，并在该对象之外保存这个状态
应用场景: 后悔药, 打游戏时的存档, 后退操作, 数据库事务管理. 保存和恢复操作, 回滚操作.

*TL;DR
Provides the ability to restore an object to its previous state.
"""

from copy import copy
from copy import deepcopy


def memento(obj, deep=False):
    """ 使用到闭包语法, 保存obj状态到state中 """
    # state存储obj的老状态或者数据
    state = deepcopy(obj.__dict__) if deep else copy(obj.__dict__)

    def restore():
        obj.__dict__.clear()  # 置空新数据
        obj.__dict__.update(state)  # 恢复老数据

    return restore


class Transaction(object):
    """A transaction guard(守卫, 警备).

    This is, in fact, just syntactic sugar(语法糖) around a memento closure.
    """

    deep = False
    states = []

    def __init__(self, deep, *targets):
        self.deep = deep
        self.targets = targets
        self.commit()

    def commit(self):
        """ 提交并保存状态 """
        self.states = [memento(target, self.deep) for target in self.targets]

    def rollback(self):
        """ 回滚并恢复老状态 """
        for a_state in self.states:
            a_state()


class Transactional(object):
    """Adds transactional semantics to methods. Methods decorated  with

    @Transactional will rollback to entry-state upon exceptions.
    往方法中添加事务语义, 一旦方法调用发生异常, 自动回滚
    """

    def __init__(self, method):
        """
        原理: 作为装饰器, 传入类方法
        @功能: 一旦调用method方法, 就会自动触发__get__, 返回一个封装过的可以保存老状态的方法
        """
        self.method = method

    def __get__(self, obj, T):
        """ 调用do_suff方法, 实际上会调用该描述符方法
        obj: 对象, 即装饰器所在的类实例对象(self)
        T: 对象类型(装饰器所在类实例对象类型)
        """
        def transaction(*args, **kwargs):
            print('装饰描述符方法')
            state = memento(obj)  # obj就是NumObj对象
            try:
                return self.method(obj, *args, **kwargs)
            except Exception as e:
                state()
                raise e

        return transaction


class NumObj(object):
    """ 真正的业务对象, 需要对该业务对象进行状态保存, 状态回滚等操作 """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<%s: %r>' % (self.__class__.__name__, self.value)

    def increment(self):
        self.value += 1

    # 将类方法传入Transactional对象中
    @Transactional
    def do_stuff(self):
        self.value = '1111'  # <- invalid value
        self.increment()  # <- will fail and rollback


def main():
    """
    >>> num_obj = NumObj(-1)
    >>> print(num_obj)
    <NumObj: -1>

    >>> a_transaction = Transaction(True, num_obj)

    >>> try:
    ...    for i in range(3):
    ...        num_obj.increment()
    ...        print(num_obj)
    ...    a_transaction.commit()
    ...    print('-- committed')
    ...    for i in range(3):
    ...        num_obj.increment()
    ...        print(num_obj)
    ...    num_obj.value += 'x'  # will fail
    ...    print(num_obj)
    ... except Exception:
    ...    a_transaction.rollback()
    ...    print('-- rolled back')
    <NumObj: 0>
    <NumObj: 1>
    <NumObj: 2>
    -- committed
    <NumObj: 3>
    <NumObj: 4>
    <NumObj: 5>
    -- rolled back

    >>> print(num_obj)
    <NumObj: 2>

    >>> print('-- now doing stuff ...')
    -- now doing stuff ...

    >>> try:
    ...    num_obj.do_stuff()
    ... except Exception:
    ...    print('-> doing stuff failed!')
    ...    import sys
    ...    import traceback
    ...    traceback.print_exc(file=sys.stdout)
    装饰描述符方法
    -> doing stuff failed!
    Traceback (most recent call last):
    ...
    TypeError: ...str...int...

    >>> print(num_obj)
    <NumObj: 2>
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
