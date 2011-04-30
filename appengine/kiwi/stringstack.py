# Kiwi string stack utilities

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

# Utilities to manage a string stack. Use this when you need a stack but must have a string.


# To push/pop values onto a string, we need a delimiter which cannot occur in the source string.
# By doubling all ~ characters, we know a single one cannot occur between two other characters.
# Then we define a multi-character delimiter that contains an undoubled ~ character.
# Delimiters go AFTER every stack entry, not between entries, so an empty stack can be
# distinguished from a stack with only an empty value on it.
pushPopDelim = "]~["

def encodeForStack(value):
    return str(value).replace("~", "~~")

def decodeFromStack(s):
    return s.replace("~~", "~")

def push(s, *values):
    """If multiple values are supplied, they are pushed on the stack in the reverse order that they are passed
    so that they are popped off in the same order as they appear and so popAllOfString returns them
    in the same order.
    """
    if not s:
        s = ""

    if len(values) > 1:
        values = list(values)
        values.reverse()
    for v in values:
        import logging
        sv = encodeForStack(v)
        s = sv + pushPopDelim + s
        
    return s
    
def pop(s, t=str):
    """Pop a value from a string stack, returning the value and the altered string"""
    value, d, s = s.partition(pushPopDelim)
    return t(decodeFromStack(value)), s

def peek(s, t=str):
    """Peek at the top value on a string stack, returning the value"""
    value, d, s = s.partition(pushPopDelim)
    return t(decodeFromStack(value))

def popAll(s):
    """Return a list of all values from a string stack. The values are returned in order from top to bottom.
    This mirrors the order of parameters if multiple values are passed to stringstack.push.
    """
    if not s:
        return []
    import logging
    result = [decodeFromStack(v) for v in s.split(pushPopDelim)[:-1]]
    return result

def count(s):
    return s.count(pushPopDelim)
    pass
