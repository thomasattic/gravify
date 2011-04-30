# Date/time conversion functions

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

import datetime

#
# DATE FUNCTIONS
#
# Long date format:  yyyy/mm/dd
# Short date format: 0aa
#

ordA = ord("a")

def make_short_date(d):
    try:
        day = (d.month - 1) * 31 + (d.day - 1)
        dayhigh = chr((day / 26) + ordA)
        daylow = chr((day % 26) + ordA)
        
        s = "%d%s%s" % (d.year - 2008, dayhigh, daylow)
        
        return s
    
    except:
        return "1aa"

def translate_short_date(shortdate):
    try:
        year = 2008 + int(shortdate[0:-2])
    
        dayhigh = ord(shortdate[-2]) - ordA
        daylow = ord(shortdate[-1]) - ordA
        day = (dayhigh * 26) + daylow
    
        return "%04d/%02d/%02d" % (year, 1 + (day / 31), 1 + (day % 31))
    
    except:
        return "2009/01/01"
    
def get_short_date(shortdate):
    try:
        year = 2008 + int(shortdate[0:-2])
    
        dayhigh = ord(shortdate[-2]) - ordA
        daylow = ord(shortdate[-1]) - ordA
        day = (dayhigh * 26) + daylow
        
        return datetime.date(year, 1 + (day / 31), 1 + (day % 31))

    except:
        return datetime.date(2009, 1, 1)