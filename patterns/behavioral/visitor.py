#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
http://peter-hoffmann.com/2010/extrinsic-visitor-pattern-python-inheritance.html

*TL;DR
Separates an algorithm from an object structure on which it operates.

行为模式--访问者模式(Visitor pattern)

访问者模式: 基于访问类来改变元素类的执行算法. 利用此方式, 元素的执行算法随着访问者改变而改变.
意图: 将数据结构和数据操作分离开来, 解决稳定的算法数据结构和易变的操作耦合度问题
应用场景:
    1. 需要对一个对象结构(逻辑意义上)中的对象进行很多不同的并且不相关的操作(放在元素类中执行),
        而需要避免让这些操作"污染"这些对象的类(访问类), 同时不希望增加新操作的时候更改这些类(访问类).
    2. 对象结构中的类很少改变, 但经常需要根据该对象定义新的操作.
    所以, 增加一个元素类, 基于这些对象来调用元素类中独立的不同操作, 达到最初的意图, 将稳定的访问类同
    具体操作区分开来.


An interesting recipe could be found in
Brian Jones, David Beazley "Python Cookbook" (2013):
- "8.21. Implementing the Visitor Pattern"
- "8.22. Implementing the Visitor Pattern Without Recursion"

*Examples in Python ecosystem:
- Python's ast.NodeVisitor: https://github.com/python/cpython/blob/master/Lib/ast.py#L250
which is then being used e.g. in tools like `pyflakes`.
- `Black` formatter tool implements it's own: https://github.com/ambv/black/blob/master/black.py#L718
"""


class Node(object):
    """ 稳定的访问类 1 """
    pass


class A(Node):
    """ 稳定的访问类 2 """
    pass


class B(Node):
    """ 稳定的访问类 3 """
    pass


class C(A, B):
    """ 稳定的访问类 4 """
    pass


class Visitor(object):
    """ 元素类 """
    def visit(self, node, *args, **kwargs):
        """ 访问入口 """
        # 根据 node 对象来决定执行何种算法
        meth = None
        for cls in node.__class__.__mro__:
            meth_name = 'visit_' + cls.__name__
            meth = getattr(self, meth_name, None)
            if meth:
                break

        if not meth:
            meth = self.generic_visit
        return meth(node, *args, **kwargs)

    def generic_visit(self, node, *args, **kwargs):
        """ 执行算法 1 """
        print('generic_visit ' + node.__class__.__name__)

    def visit_B(self, node, *args, **kwargs):
        """ 执行算法 2 """
        print('visit_B ' + node.__class__.__name__)


def main():
    """
    >>> a, b, c = A(), B(), C()
    >>> visitor = Visitor()

    >>> visitor.visit(a)
    generic_visit A

    >>> visitor.visit(b)
    visit_B B

    >>> visitor.visit(c)
    visit_B C
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
