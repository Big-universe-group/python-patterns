#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*What is this pattern about?

In Java and other languages, the Abstract Factory Pattern serves to provide an interface for
creating related/dependent objects without need to specify their
actual class.

The idea is to abstract the creation of objects depending on business
logic, platform choice, etc.

In Python, the interface we use is simply a callable, which is "builtin" interface
in Python, and in normal circumstances we can simply use the class itself as
that callable, because classes are first class objects in Python.

*What does this example do?
This particular implementation abstracts the creation of a pet and
does so depending on the factory we chose (Dog or Cat, or random_animal)
This works because both Dog/Cat and random_animal respect a common
interface (callable for creation and .speak()).
Now my application can create pets abstractly and decide later,
based on my own criteria, dogs over cats.

*Where is the pattern used practically?

创建型模式--抽象工厂(abstract factory)
抽象工厂模式: 围绕一个超级工厂创建其他"一线工厂", 该超级工厂被称为其他"一线工厂"的工厂. 接口是一个
    负责创建相关对象的"工厂", 无需显示的指定类. 每一个生成的"一线工厂"都按照"工厂模式"来提供真正需要的对象.

使用场景: 系统产品里面有多于一个的产品镞, 例如参加聚会时的穿着(商务装, 时尚装), 利用OOP 思想来创建某一类
    的产品.


*References:
https://sourcemaking.com/design_patterns/abstract_factory
http://ginstrom.com/scribbles/2007/10/08/design-patterns-python-style/

*TL;DR
Provides a way to encapsulate a group of individual factories.
"""

import random


class PetShop(object):
    """A pet shop
    抽象工厂: 宠物商店, 出售多种类的宠物对象(每一个种类有多个对象)
    """

    def __init__(self, animal_factory=None):
        """pet_factory is our abstract factory.  We can set it at will."""
        # 指定需要创建的宠物种类
        self.pet_factory = animal_factory

    def show_pet(self):
        """Creates and shows a pet using the abstract factory: 相当于创建宠物对象"""
        pet = self.pet_factory()
        print("We have a lovely {}".format(pet))
        print("It says {}".format(pet.speak()))


class Dog(object):
    def speak(self):
        return "woof"

    def __str__(self):
        return "Dog"


class Cat(object):
    def speak(self):
        return "meow"

    def __str__(self):
        return "Cat"


# Additional factories:

# Create a random animal
def random_animal():
    """Let's be dynamic!"""
    return random.choice([Dog, Cat])()


# Show pets with various factories
if __name__ == "__main__":
    # A Shop that sells only cats
    cat_shop = PetShop(Cat)  # 宠物抽象工厂, 接收某一类宠物并批量创建此类宠物对象
    cat_shop.show_pet()  # 返回宠物对象
    print("")

    # A shop that sells random animals
    shop = PetShop(random_animal)
    for i in range(3):
        shop.show_pet()
        print("=" * 20)


### OUTPUT ###
# We have a lovely Cat
# It says meow
#
# We have a lovely Dog
# It says woof
# ====================
# We have a lovely Cat
# It says meow
# ====================
# We have a lovely Cat
# It says meow
# ====================
