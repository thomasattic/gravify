# Form handling utilities

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

def getInputValue(values, name, emptyValue=None):
    """Returns the value of a HTML form value or None if there is no such value or the field was empty.
    If emptyValue is supplied, it is the return value when the field is empty"""
    if name in values:
        result = values[name]
        if result.strip() == "": return emptyValue
        return unicode(result, "utf-8")
    return emptyValue

def getBooleanValue(values, name, emptyValue=None):
    """Returns the value of a boolean form value as True or False, or None if there is no such field value."""
    val = getInputValue(values, name)
    if val is None: return emptyValue
    val = val.lower()
    if (val == "true" or val == "1"): return True
    return False

def getIntegerValue(values, name, emptyValue=None):
    """Returns the value of an integer form value as True or False, or None if there is no such field value."""
    val = getInputValue(values, name)
    if val is None: return emptyValue
    if not val.isdigit(): return emptyValue
    return int(val)

def getCheckboxValue(values, name):
    """Returns the value of a HTML form checkbox as a boolean.
    
    Never returns None
    """
    return True if name in values else False
