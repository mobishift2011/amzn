#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" testing matching functions """
from backends.matching.extractor import Extractor

e = Extractor(tags=['One','Two','Three','Th'])    

def test_simple_extract():
    assert e.extract('One') == ['One']

def test_multiple_match():
    assert e.extract('One,Two') == ['One','Two']

def test_case_insensitive():
    assert e.extract('one,Two') == ['One','Two']

def test_word_boundary_aware():
    assert e.extract('onetwoth') == []

def test_word_boundaries_allowed():
    assert e.extract('one ,.2 32two') == ['One','Two']

