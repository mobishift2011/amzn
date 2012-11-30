#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from mongoengine import *
connect("test")

class A(Document):
    a = StringField(primary_key=True)
    b = DictField()

aa = A(a='who')
aa.b = {'1': 2}
aa.save()
