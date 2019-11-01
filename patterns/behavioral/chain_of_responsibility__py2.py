#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*What is this pattern about?

行为模式 --- 责任链模式
责任链模式（Chain of Responsibility Pattern）为请求创建了一个接收者对象的链, 对请求的发送者和接收者进行解耦.

通常每个接收者都包含对另一个接收者的引用, 如果一个对象不能处理该请求, 那么它会把相同的请求传给下一个接收者.

使用场景:  有多个对象可以处理同一个请求, 具体哪个对象处理该请求由运行时刻自动确定; 可动态指定一组对象处理请求

The Chain of responsibility(责任链) is an object oriented version(定向的) of the
`if ... elif ... elif ... else ...` idiom(习惯用法), with the
benefit that the condition–action blocks(条件动作块) can be dynamically rearranged(动态重新排列)
and reconfigured at runtime.

This pattern aims(目的宗旨) to decouple(解耦) the senders of a request from its
receivers by allowing request to move through chained
receivers until it is handled.

Request receiver in simple form(简单形式) keeps a reference to a single successor(后继者).
As a variation some receivers may be capable(能力资格) of sending requests out
in several directions, forming a `tree of responsibility`.

*TL;DR
Allow a request to pass down a chain of receivers until it is handled.
"""

import abc


class Handler(object):
    """ 处理程序基类或者接口 """
    __metaclass__ = abc.ABCMeta

    def __init__(self, successor=None):
        # 后继者, 这是指向联调的后一个实例对象
        self.successor = successor

    def handle(self, request):
        """
        Handle request and stop.
        If can't - call next handler in chain.

        As an alternative you might even in case of success
        call the next handler.
        """
        res = self.check_range(request)
        if not res and self.successor:
            # 处理失败, 将请求放入链下一个后继者中处理
            self.successor.handle(request)
        else:
            # 处理成功, 直接返回
            pass

    @abc.abstractmethod
    def check_range(self, request):
        """Compare passed value to predefined interval"""


class ConcreteHandler0(Handler):
    """Each handler can be different 处理程序 1.
    Be simple and static...
    """

    @staticmethod
    def check_range(request):
        if 0 <= request < 10:
            print("request {} handled in handler 0".format(request))
            return True


class ConcreteHandler1(Handler):
    """... With it's own internal state"""

    start, end = 10, 20

    def check_range(self, request):
        if self.start <= request < self.end:
            print("request {} handled in handler 1".format(request))
            return True


class ConcreteHandler2(Handler):
    """... With helper methods."""

    def check_range(self, request):
        start, end = self.get_interval_from_db()
        if start <= request < end:
            print("request {} handled in handler 2".format(request))
            return True

    @staticmethod
    def get_interval_from_db():
        return (20, 30)


class FallbackHandler(Handler):
    """ 最后的错误处理 """
    @staticmethod
    def check_range(request):
        print("end of chain, no handler for {}".format(request))
        return False


def main():
    """
    >>> h0 = ConcreteHandler0()
    >>> h1 = ConcreteHandler1()
    >>> h2 = ConcreteHandler2(FallbackHandler())
    >>> h0.successor = h1
    >>> h1.successor = h2

    >>> requests = [2, 5, 14, 22, 18, 3, 35, 27, 20]
    >>> for request in requests:
    ...     h0.handle(request)
    request 2 handled in handler 0
    request 5 handled in handler 0
    request 14 handled in handler 1
    request 22 handled in handler 2
    request 18 handled in handler 1
    request 3 handled in handler 0
    end of chain, no handler for 35
    request 27 handled in handler 2
    request 20 handled in handler 2
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
