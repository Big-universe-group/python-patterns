#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
An example of the Template pattern in Python

行为模式--模板模式(Template pattern)
模板模式: 一个抽象类公开定义了执行它的方法的方式/模板, 子类可以按需要重写方法实现,
        但调用将以抽象类中定义的方式进行
意图: 定义一个操作中的算法的骨架, 而将一些步骤延迟到子类中, 从而在前期搭建好基本框架的基础上, 后期
        子类在保持基本逻辑基础上可以进行某些特殊的处理.

*TL;DR
Defines the skeleton of a base algorithm, deferring definition of exact
steps to subclasses.

*Examples in Python ecosystem:
Django class based views: https://docs.djangoproject.com/en/2.1/topics/class-based-views/
"""


def get_text():
    return "plain-text"


def get_pdf():
    return "pdf"


def get_csv():
    return "csv"


def convert_to_text(data):
    print("[CONVERT]")
    return "{} as text".format(data)


def saver():
    print("[SAVE]")


def template_function(getter, converter=False, to_save=False):
    data = getter()
    print("Got `{}`".format(data))

    if len(data) <= 3 and converter:
        data = converter(data)
    else:
        print("Skip conversion")

    if to_save:
        saver()

    print("`{}` was processed".format(data))


def main():
    """
    >>> template_function(get_text, to_save=True)
    Got `plain-text`
    Skip conversion
    [SAVE]
    `plain-text` was processed

    >>> template_function(get_pdf, converter=convert_to_text)
    Got `pdf`
    [CONVERT]
    `pdf as text` was processed

    >>> template_function(get_csv, to_save=True)
    Got `csv`
    Skip conversion
    [SAVE]
    `csv` was processed
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
