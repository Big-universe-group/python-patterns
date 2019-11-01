#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
行为模式--注册表模式(注册器模式, 有些将其归类到结构性模式中)

注册表模式: 把多个类的实例注册到一个注册器类中去，然后需要哪个类，由这个注册器类统一调取
实现方式: 通常通过单例模式来实现注册表模式
意图: 解决常用对象的存放问题，实现类似于全局变量的功能
"""


class RegistryHolder(type):

    REGISTRY = {}  # 注册表(全局唯一性对象)

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        """
            Here the name of the class is used as key but it could be any class
            parameter.
        """
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)


class BaseRegisteredClass(object):
    """
    Any class that will inherits from BaseRegisteredClass will be included
    inside the dict RegistryHolder.REGISTRY, the key being the name of the
    class and the associated value, the class itself.
    相当于注册方法基类
    """
    # __metaclass__使用元类创建对象, 每一次实例化类对象时都会自动调用RegistryHolder中的
    # __new__方法.
    __metaclass__ = RegistryHolder


def main():
    """
    Before subclassing
    >>> sorted(RegistryHolder.REGISTRY)
    ['BaseRegisteredClass']

    >>> class ClassRegistree(BaseRegisteredClass):
    ...    def __init__(self, *args, **kwargs):
    ...        pass

    After subclassing
    >>> sorted(RegistryHolder.REGISTRY)
    ['BaseRegisteredClass', 'ClassRegistree']
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
