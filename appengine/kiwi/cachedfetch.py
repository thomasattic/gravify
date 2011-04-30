# Cached URL fetching

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

"""
URL Handler that fetches an external URL and then caches the contents.
"""

from google.appengine.api import urlfetch

import kiwioptions
import cache

def fetch(url, time=0):
    """Fetch a URL, caching the result"""

    result = cache.get(url, namespace="kiwi.f")
    if result:
        return result

    try:
        fetchResult = urlfetch.fetch(url)
        if fetchResult.status_code == 200:
            result = fetchResult.content
            cache.set(url, result, time=time, namespace="kiwi.f")
            return result
    except:
        pass
    
    return ""
