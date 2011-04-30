# Object utilities for Kiwi

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

def make_instance_method(obj, name, f, knownmethodname="__init__"):
    """
    Adds a bound instance method to an object with a given name.
    Like all instance methods, the function to be assigned must have a first parameter of self.
    If the class does not have an __init__ method, then name of a method defined by the class
    must be supplied.    
    """
    #
    # objtype = type(obj)
    # knownmethod = dir(obj.__class__)[0]
    # boundtype = type(obj.__class__.[knownmethod])
    # obj.[name] = boundtype(f, obj, objtype)
    return eval("type(obj.__class__.%(knownmethod)s)(f, obj, type(obj))" % { "name": name, "knownmethod": knownmethodname })              
