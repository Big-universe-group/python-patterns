#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
行为模式--订阅发布模式(有点类似观察者模式)
订阅发布模式: 一对多模式, 其中一表示发布者, 多表示订阅者, 一旦发布者发布内容更新, 会通知订阅者
使用场景: 大部分的队列都使用这个模式, 已低耦合度来进行数据的通知和数据的处理

Reference:
http://www.slideshare.net/ishraqabd/publish-subscribe-model-overview-13368808
Author: https://github.com/HanWenfang
"""


class Provider:
    def __init__(self):
        self.msg_queue = []
        self.subscribers = {}

    def notify(self, msg):
        # 在 MQ 中, 这里是直接发送信号, 或者将信息推入队列中
        self.msg_queue.append(msg)

    def subscribe(self, msg, subscriber):
        """ 订阅 """
        self.subscribers.setdefault(msg, []).append(subscriber)

    def unsubscribe(self, msg, subscriber):
        """ 取消订阅 """
        self.subscribers[msg].remove(subscriber)

    def update(self):
        for msg in self.msg_queue:
            for sub in self.subscribers.get(msg, []):
                sub.run(msg)
        self.msg_queue = []


class Publisher:
    """ Provider的代理人, 实际上内容生产者为provider """
    def __init__(self, msg_center):
        self.provider = msg_center

    def publish(self, msg):
        self.provider.notify(msg)


class Subscriber:
    def __init__(self, name, msg_center):
        self.name = name
        self.provider = msg_center

    def subscribe(self, msg):
        self.provider.subscribe(msg, self)

    def unsubscribe(self, msg):
        self.provider.unsubscribe(msg, self)

    def run(self, msg):
        print("{} got {}".format(self.name, msg))


def main():
    # 1. 内容提供者或者生产者, 依托于publisher来进行消息的通知
    message_center = Provider()
    fftv = Publisher(message_center)

    # 2. 内容订阅者
    jim = Subscriber("jim", message_center)
    jim.subscribe("cartoon")
    jack = Subscriber("jack", message_center)
    jack.subscribe("music")
    gee = Subscriber("gee", message_center)
    gee.subscribe("movie")
    vani = Subscriber("vani", message_center)
    vani.subscribe("movie")
    vani.unsubscribe("movie")

    fftv.publish("cartoon")
    fftv.publish("music")
    fftv.publish("ads")
    fftv.publish("movie")
    fftv.publish("cartoon")
    fftv.publish("cartoon")
    fftv.publish("movie")
    fftv.publish("blank")

    message_center.update()


if __name__ == "__main__":
    main()


OUTPUT = """
jim got cartoon
jack got music
gee got movie
jim got cartoon
jim got cartoon
gee got movie
"""
