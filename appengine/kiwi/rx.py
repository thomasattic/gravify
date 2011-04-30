# Kiwi named and cached compiled regular expressions

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

import re

dict = {}

def exists(name):
    """Test if a named regular expression is in the cache"""
    return name in dict

def define(name, regex):
    """Define a named regular expression, replacing any previously existing one"""
    rxc = re.compile(regex)
    dict[name] = rxc
    return rxc

def match(name, s, regex=None):
    """Match a named regular expression, optionally defining it if it doesn't already exist"""
    if regex and name not in dict:
        rxc = define(name, regex)
    else:
        rxc = dict[name]
    return rxc.match(s)

def search(name, s, regex=None):
    """Search for a named regular expression, optionally defining it if it doesn't already exist"""
    if regex and name not in dict:
        rxc = define(name, regex)
    else:
        rxc = dict[name]
    return rxc.search(s)

def sub(name, repl, s, count=0, regex=None):
    """Do a regex replacement using a named regular expression, optionally defining it if it doesn't already exist"""
    if regex and name not in dict:
        rxc = define(name, regex)
    else:
        rxc = dict[name]
    return rxc.sub(repl, s, count)

def clear():
    """Clear all named regular expressions"""
    dict = {}
