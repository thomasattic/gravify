# Kiwi numeric conversion for URL shortening

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

charset = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

def number_to_string(n):
    result = ""
    n = abs(n)
    while n > 0:
        result += charset[n % 32]
        n /= 32
        
    return result
    
def string_to_number(s):
    result = 0
    for i in range(len(result)-1, 0, -1):
        n = charset.find(s[i])
        if n == -1: return -1
        result = result * 32 + n
        
    return result
