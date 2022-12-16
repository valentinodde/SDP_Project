#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 11:17:18 2022

@author: valentin
"""


import json

def load_small_data():
    with open('data/toy_instance.json') as f:
        js = json.load(f)
    return js

def load_medium_data():
    with open('data/medium_instance.json') as f:
        js = json.load(f)
    return js


def load_big_data():
    with open('data/large_instance.json') as f:
        js = json.load(f)
    return js