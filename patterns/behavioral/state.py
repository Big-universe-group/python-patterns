#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implementation of the state pattern

行为模式--状态模式

状态模式: 类的行为是基于它的状态改变的, 允许对象在状态改变时更改行为, 看起来更改了类结构
主要解决: 对象的行为依赖于它的状态(属性), 并且可以根据它的状态改变而改变它的相关行为. 该模式
    用以解决代码中包含大量与对象状态有关的条件语句(if..else), 命令模式和规范模式在一定程度上也解决此类问题.
    通过将各种具体的状态类抽象出来, 后续根据外在表现类中不同的函数指向各种不同的状态, 比如:
        + 我要吃饭: 指向吃饭类
        + 我要运动: 指向运动类
    但是对外表现为一个"人"类.
使用场景: 行为随状态改变而改变的场景; 条件/分支语句的代替者(另外一个是规范模式).
有点: 封装了转换规则; 枚举可能状态; 将所有与某一个行为相关的所有状态全部放到一个类中.

注意: 规范模式解决if-else语句, 状态模式解决和对象状态相关的大量判断条件

http://ginstrom.com/scribbles/2007/10/08/design-patterns-python-style/

*TL;DR
Implements state as a derived class of the state pattern interface.
Implements state transitions by invoking methods from the pattern's superclass.
"""

from __future__ import print_function


class State(object):
    """Base state. This is to share functionality"""
    def scan(self):
        """Scan the dial to the next station"""
        # 每一次调用都会更改类中的特定属性(状态)
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print(u"Scanning... Station is %s %s" % (self.stations[self.pos], self.name))


class AmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos = 0
        self.name = "AM"

    def toggle_amfm(self):
        # 切换
        print(u"Switching to FM")
        self.radio.state = self.radio.fmstate


class FmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos = 0
        self.name = "FM"

    def toggle_amfm(self):
        # 切换
        print(u"Switching to AM")
        self.radio.state = self.radio.amstate


class Radio(object):
    """A radio.     It has a scan button, and an AM/FM toggle switch.
    @状态模式: 每次函数调用的副作用都会直接影响/叠加到类本身对象身上.
    """
    def __init__(self):
        """We have an AM state and an FM state"""
        self.amstate = AmState(self)
        self.fmstate = FmState(self)
        # self.state随着toggle_amfm的调用, 会指向不同的实例对象, 对外表现出来整个功能的变动
        self.state = self.amstate

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()


# Test our radio out
def main():
    radio = Radio()
    # [radio.scan] * 2 变为 [radio.scan, radio.scan]
    actions = [radio.scan] * 2 + [radio.toggle_amfm] + [radio.scan] * 2
    actions *= 2
    # 一个有着同一个类各种状态函数, 其中状态函数还可能类同的列表
    for action in actions:
        action()  # 调用函数


if __name__ == '__main__':
    main()


OUTPUT = """
Scanning... Station is 1380 AM
Scanning... Station is 1510 AM
Switching to FM
Scanning... Station is 89.1 FM
Scanning... Station is 103.9 FM
Scanning... Station is 81.3 FM
Scanning... Station is 89.1 FM
Switching to AM
Scanning... Station is 1250 AM
Scanning... Station is 1380 AM
"""
