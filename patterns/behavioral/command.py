#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*TL;DR
Encapsulates(封装) all information needed to perform an action(执行动作) or trigger an event(触发事件).

行为模式--命令行模式
命令行模式: 请求以命令的形式包含在对象中, 并传给对象, 调用对象会寻找可以处理该命令的相应对象并执行命令
意图: 将一个请求封装成一个对象，从而使您可以用不同的请求对客户进行参数化, 一定程度上解决if..else问题
使用场景:
    比如要对行为进行"记录、撤销/重做、事务"等处理, 此时需要将"行为请求者"与"行为实现者"解耦.
    received: 命令真正执行者
    command: 作为命令本身
    invoker: 使用命令对象的入口, 请求本身作为一个对象

    调用者知道各种命令的执行者集群; 但是为了降低耦合度, 调用方仅仅调用invoker, 通过command本身来将
    命令传给received进行处理.

命令模式的关键: 引入抽象命令接口, 发送者针对抽象命令接口编程

*Examples in Python ecosystem:
Django HttpRequest (without `execute` method):
 https://docs.djangoproject.com/en/2.1/ref/request-response/#httprequest-objects

例如django将所有请求行为抽象为HttpRequest(命令接口), 之后利用request来获取行为或者进行其他操作.
例如django将所有响应行为抽象为HttpResponse, 利用response获取各类结果
"""

from __future__ import print_function
import os
import shutil


class CopyFileCommand(object):
    """功能: 拷贝文件
    """
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def execute(self):
        """ 执行 """
        self.copy(self.src, self.dest)

    def undo(self):
        """ 撤销 """
        self.remove(self.dest)

    def copy(self, src, dest):
        print(u"copy %s to %s" % (src, dest))
        shutil.copyfile(src, dest)

    def remove(self, dest):
        print("remove {}".format(dest))
        os.remove(dest)


class MoveFileCommand(object):
    """
    功能: 移动文件
    行为实现者: execute, undo, 自动寻找适合该命令的操作对象并执行动作
    """
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def execute(self):
        """ 执行 """
        self.rename(self.src, self.dest)

    def undo(self):
        """ 撤销 """
        self.rename(self.dest, self.src)

    def rename(self, src, dest):
        print(u"renaming %s to %s" % (src, dest))
        os.rename(src, dest)


def main():
    """
    >>> from os.path import lexists

    # 命令集群(invoker)
    >>> command_stack = [
    ...     MoveFileCommand('foo.txt', 'bar.txt'),
    ...     MoveFileCommand('bar.txt', 'baz.txt')
    ...     CopyFileCommand('bar.txt', 'baz2.txt')
    ... ]

    # Verify that none of the target files exist
    >>> assert not lexists("foo.txt")
    >>> assert not lexists("bar.txt")
    >>> assert not lexists("baz.txt")

    # Create empty file
    >>> open("foo.txt", "w").close()

    # Commands can be executed later on
    >>> for cmd in command_stack:
    ...     cmd.execute()
    renaming foo.txt to bar.txt
    renaming bar.txt to baz.txt
    copy bar.txt to baz2.txt

    # And can also be undone at will
    >>> for cmd in reversed(command_stack):
    ...     cmd.undo()
    renaming baz.txt to bar.txt
    renaming bar.txt to foo.txt
    remove bar2.txt

    >>> os.unlink("foo.txt")
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
