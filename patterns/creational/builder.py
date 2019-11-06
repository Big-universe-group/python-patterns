#!/usr/bin/python
# -*- coding : utf-8 -*-

"""
*What is this pattern about?
It decouples the creation of a complex object and its representation,
so that the same process can be reused to build objects from the same
family.
This is useful when you must separate the specification of an object
from its actual representation (generally for abstraction).

*What does this example do?

The first example achieves this by using an abstract base
class for a building, where the initializer (__init__ method) specifies the
steps needed, and the concrete subclasses implement these steps.

In other programming languages, a more complex arrangement is sometimes
necessary. In particular, you cannot have polymorphic behaviour in a constructor in C++ -
see https://stackoverflow.com/questions/1453131/how-can-i-get-polymorphic-behavior-in-a-c-constructor
- which means this Python technique will not work. The polymorphism
required has to be provided by an external, already constructed
instance of a different class.

In general, in Python this won't be necessary, but a second example showing
this kind of arrangement is also included.


创建型模式--建造者模式(builder pattern)
建造者模式: 使用多个简单的对象一步步构建一个复杂的对象.
意图: 将一个复杂的构建和其表示分离开来, 是的相同的构建过程可以创建不同的表示
解决问题: 面临着"一个复杂对象"的创建工作, 其通常由各个部分的子对象用一定的算法构成.
        由于需求的变化, 这个复杂对象的各个部分经常面临着剧烈的变化, 但是将它们组合在一起的算法却相对稳定

应用场景: 肯德基套餐是不变的, 但是里面的汉堡, 薯条等成分一直在变; Java的 StringBuilder.

和工厂模式区别: 建造者模式更加关注与零件装配的顺序


*Where is the pattern used practically?

*References:
https://sourcemaking.com/design_patterns/builder

*TL;DR
Decouples the creation of a complex object and its representation.
"""


# Abstract Building
class Building(object):
    """ 构建者父类: 维持两个基本的构建过程(build_floor, build_size) """
    def __init__(self):
        self.build_floor()
        self.build_size()

    def build_floor(self):
        raise NotImplementedError

    def build_size(self):
        raise NotImplementedError

    def __repr__(self):
        return 'Floor: {0.floor} | Size: {0.size}'.format(self)


# Concrete Buildings
class House(Building):
    """ 普通意义房子, 别墅 """
    def build_floor(self):
        self.floor = 'One'

    def build_size(self):
        self.size = 'Big'


class Flat(Building):
    """ 套间; 住宅房子; 平面 """
    def build_floor(self):
        self.floor = 'More than One'

    def build_size(self):
        self.size = 'Small'


# In some very complex cases, it might be desirable to pull out the building
# logic into another function (or a method on another class), rather than being
# in the base class '__init__'. (This leaves you in the strange situation where
# a concrete class does not have a useful constructor)


class ComplexBuilding(object):
    """ 另外一个构建方式, 没有在初始化的是就开始进行构建 """
    def __repr__(self):
        return 'Floor: {0.floor} | Size: {0.size}'.format(self)


class ComplexHouse(ComplexBuilding):
    def build_floor(self):
        self.floor = 'One'

    def build_size(self):
        self.size = 'Big and fancy'


def construct_building(cls):
    # 所有对象构建流程都是一样的: build_floor + build_size
    building = cls()
    building.build_floor()
    building.build_size()
    return building


# Client
if __name__ == "__main__":
    # 方式 1: 在初始化的时候就完成构建
    house = House()
    print(house)
    flat = Flat()
    print(flat)

    # 方式 2: 通过调用来进行构建工作
    # Using an external constructor function:
    complex_house = construct_building(ComplexHouse)
    print(complex_house)

### OUTPUT ###
# Floor: One | Size: Big
# Floor: More than One | Size: Small
# Floor: One | Size: Big and fancy
