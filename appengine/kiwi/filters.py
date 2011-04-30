# Django template filters

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

from django import template
from django.template.defaultfilters import stringfilter
from google.appengine.ext import webapp

import signatures
 
register = webapp.template.create_template_register()
# NOTE: These are actually registered in main.py
# It may be that I don't need to do it this way and instead I should do: register = template.Library()
    
# FUTURE: This is superceded by an equivalent filter in Django 1.0
@stringfilter
@register.filter
def escapejs(s, arg=None):
    """Escape a string for JavaScript or JSON"""
    
    if not s: return ''

    s = str(s).replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r").replace('"', '\\"')
        
    return s

escapejs.is_safe = True

@stringfilter
@register.filter
def jsquote(s, arg=None):
    """Quote a string for JavaScript or JSON"""
    
    return '"%s"' % escapejs(s, arg)

jsquote.is_safe = True

@stringfilter
@register.filter
def bool(value, arg=None):
    if value: return "true"
    return "false"

bool.is_safe = True

@stringfilter
@register.filter
def clean(name, arg=None):
    """Reduce a string to something safe for an HTML identifier"""
    
    if not name: return ""

    result = []

    for c in name.lower():
        if c.isalnum(): result.append(c)
        
    return "".join(result)

clean.is_safe = True

@stringfilter
@register.filter
def cleancolor(value, arg=None):
    """Reduce a string to something safe for an HTML color (# at the beginning is allowed)"""
    
    if not value: return ""

    result = []

    if value.startswith("#"):
        result = ["#"]
        value = value[1:]
        
    for c in value.lower():
        if c.isalnum(): result.append(c)
        
    return "".join(result)

cleancolor.is_safe = True

@register.filter
def repeat(n, arg=None):
    """Repeat the argument string a number of times"""

    if not arg: return ""
    try:
        n = int(n)
    except:
        return arg
    
    return str(arg) * n

repeat.is_safe = True

@register.filter
def multiply(n, arg="1"):
    """Multiple the value times the argument"""

    if not arg: return ""
    try:
        n = int(n)
        arg = int(arg)
    except:
        return ""
    
    return n * arg

multiply.is_safe = True

@stringfilter
@register.filter
def signed(s, arg=None, hide=False):
    """Sign a string, optionally with a time limit in minutes. The signed result contains the original string."""

    if not arg:
        n = 60
    else:
        try:
            n = int(arg)
        except:
            n = 60

    return signatures.sign(s, minutes=n, hide=hide)

@stringfilter
@register.filter
def signedhidden(s, arg=None):
    """Sign a string, optionally with a time limit in minutes. The signed result does not contain the original string."""
    return signed(s, arg, hide=True)
