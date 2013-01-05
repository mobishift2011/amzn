#!/usr/bin/env python
# -*- coding: utf-8 -*-
from helpers.signals import SignalQueue, Signal

# site, method
run_command = SignalQueue("run_command")

# auto=True/False
auto_scheduling = SignalQueue("auto_scheduling")
