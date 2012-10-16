#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""用回调来去除程序耦合

例如：

1.在任务结束的时候发送结束信号:
>>> import signals
>>> signals.signal("taskcomplete", product_id=1, time_consumed=5.23)

2.在任务统计模块(如果有这个模块的话)收集信息并处理:
>>> import signals
>>> @signals.bind("taskcomplete")
>>> def log_task(product_id, time_consumed):
...     print("任务{product_id}在{time_consumed}秒内成功执行".format(**locals()))

则每次任务结束以后会自动输出任务完成信息

"""
import logging
from collections import defaultdict
from multiprocessing import current_process

class Processer:
    def __init__(self):
        self.workers = defaultdict(set)
        self.funcnames = set()

    def add_worker(self, workername, callback):
        funcname = callback.__name__
        if funcname not in self.funcnames:
            self.workers[workername].add(callback)
            self.funcnames.add(funcname)

    def _execute_callbacks(self, workername, message):
        if workername not in self.workers:
            logging.warning("不存在名为%s的信号接收函数!"%workername)
        else:
            try:
                data = message
                for w in self.workers[workername]:
                    w(*data['args'],**data['kwargs'])
            except Exception, e:
                logging.exception("消息处理出错")
                logging.error("workername, %s" % workername)
                logging.error("message, %s" % message)

    def send_message(self, workername, message):
        self._execute_callbacks(workername, message)

p = Processer()

def bind(workername):
    """ the decorator method for convinience """
    def _decorator(f):
        p.add_worker(str(workername), f)
        return f
    return _decorator

def signal(workername, *args, **kwargs):
    data = {'args':args,'kwargs':kwargs}
    p.send_message(workername, data)

if __name__ == '__main__':
    has_item = "has_item"

    @bind(has_item)
    def when_fight_finished_print_signal(tip, aid):
        print( "tip is {tip} and aid is {aid}".format(**locals()))

    signal(has_item, 'wow', aid=1)

