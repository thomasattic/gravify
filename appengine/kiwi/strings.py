# Kiwi string utilities

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

def parse_options(options):
    """Parse a set of options in the format 'name=value;name=value;...' and return a dict"""
    result = {}
    for opt in options.split(","):
        if "=" in opt:
            try:
                (name, value) = opt.split("=")
                result[name] = value
            except:
                pass
        else:
            result[opt] = ""
    return result

def findany(s, chars, start=0, charPriority=False):
    """Find any of the specified characters in the string, returning the position of the first one found.
    By default, finds the first char in the string that is in chars.
    If charPriority is true, finds the first char in chars that is anywhere in the string.
    """
    result = None
    if charPriority:
        for c in chars:
            pos = s.find(c, start)
            if pos != -1:
                return pos
    else:
        pos = start
        while pos < len(s):
            c = s[pos]
            if c in chars:
                return pos

    return -1  

def replaceany(s, oldstrings, new):
    """Find any of the specified strings in the specified string, replace all of them with the new string
    If oldstrings is a single string instead of an array, each character in it is replaced with the new string
    """
    for old in oldstrings:
        if old in s:
            s = s.replace(old, new)
            
    return s

def escapechars(s, charlist, escapechar="\\"):
    """Escape any of the characters in charlist with a hex escape sequence
    """
    if escapechar in s:
        e = "%sx%02x" % (escapechar, ord(escapechar))
        s = s.replace(escapechar, e)
    for c in charlist:
        if c in s and c != escapechar:
            e = "%sx%02x" % (escapechar, ord(c))
            s = s.replace(c, e)
    return s

def unescapechars(s, charlist, escapechar="\\"):
    """Reverse the effect of escapechars
    """
    if escapechar in s:
        for c in charlist:
            if c != escapechar:
                e = "%sx%02x" % (escapechar, ord(c))
                if e in s:
                    s = s.replace(e, c)
        e = "%sx%02x" % (escapechar, ord(escapechar))
        if e in s:
            s = s.replace(e, escapechar)
    return s
