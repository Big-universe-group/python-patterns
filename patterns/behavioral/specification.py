#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Gordeev Andrey <gordeev.and.and@gmail.com>

行为模式--规约模式(Specification Pattern)

规约模式: 用来将业务规则(一般为隐式业务规则)封装成独立的逻辑单元，从而将隐式业务规则提炼为显示概念，
    并达到代码复用的目的
隐式业务规则: 例如网站目标业务对象为 18 岁以上, 则 18 岁以下的判断条件就是隐式业务规则
显示概念: 将代码中的隐式业务规则提出来, 解耦, 避免代码改动导致的后续问题

DDD: 领域驱动设计, 通常需要进行大量的业务知识梳理，而后到达软件设计的层面，最后才是开发。
    而在业务知识梳理的过程中，我们必然会形成某个领域知识，根据领域知识来一步步驱动软件设计,
    就是领域驱动设计的基本概念

使用场景: 业务规则不会仅仅验证一下年龄这么简单，例如订单提交，你可能需要验证用户账号是否可用、
    订单商品的库存是否满足预定量、配送地址是否完整. 这一系列的隐式业务规则不能通过一个个条件判断
    在代码中写死, 这样不利于代码的维护, 需要提炼出来.(DDD--领域驱动设计)

*TL;DR
Provides recombination business logic by chaining together using boolean logic.
"""

from abc import abstractmethod


class Specification(object):
    def and_specification(self, candidate):
        raise NotImplementedError()

    def or_specification(self, candidate):
        raise NotImplementedError()

    def not_specification(self):
        raise NotImplementedError()

    @abstractmethod
    def is_satisfied_by(self, candidate):
        pass


class CompositeSpecification(Specification):
    """ Composite: 合成 """
    @abstractmethod
    def is_satisfied_by(self, candidate):
        pass

    def and_specification(self, candidate):
        return AndSpecification(self, candidate)

    def or_specification(self, candidate):
        return OrSpecification(self, candidate)

    def not_specification(self):
        return NotSpecification(self)


class AndSpecification(CompositeSpecification):
    _one = Specification()
    _other = Specification()

    def __init__(self, one, other):
        self._one = one
        self._other = other

    def is_satisfied_by(self, candidate):
        return bool(self._one.is_satisfied_by(candidate) and self._other.is_satisfied_by(candidate))


class OrSpecification(CompositeSpecification):
    _one = Specification()
    _other = Specification()

    def __init__(self, one, other):
        self._one = one
        self._other = other

    def is_satisfied_by(self, candidate):
        return bool(self._one.is_satisfied_by(candidate) or self._other.is_satisfied_by(candidate))


class NotSpecification(CompositeSpecification):
    _wrapped = Specification()

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def is_satisfied_by(self, candidate):
        return bool(not self._wrapped.is_satisfied_by(candidate))


class User(object):
    def __init__(self, super_user=False):
        self.super_user = super_user


class UserSpecification(CompositeSpecification):
    def is_satisfied_by(self, candidate):
        return isinstance(candidate, User)


class SuperUserSpecification(CompositeSpecification):
    def is_satisfied_by(self, candidate):
        return getattr(candidate, 'super_user', False)


def main():
    print('Specification')
    andrey = User()
    ivan = User(super_user=True)
    vasiliy = 'not User instance'

    root_specification = UserSpecification().and_specification(SuperUserSpecification())

    print(root_specification.is_satisfied_by(andrey))
    print(root_specification.is_satisfied_by(ivan))
    print(root_specification.is_satisfied_by(vasiliy))


if __name__ == '__main__':
    main()


OUTPUT = """
Specification
False
True
False
"""
