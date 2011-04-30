# Kiwi URL handlers

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""


from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template.loader import render_to_string

import kiwioptions
import cachedfetch

# BOGUS - Need documentation

def redirect(req, **params):
    """Redirect handler for URLs"""

    if "url" in params:
        url = params["url"]
    else:
        url = "/"
        
    if "%" in url:
        try:
            url = url % params
        except:
            pass
        
    if "permanent" in params and params["permanent"]:
        return HttpResponsePermanentRedirect(url)
    return HttpResponseRedirect(url)
    
def fetch(req, **params):
    """Fetch handler for URLs - fetches the contents of a page and caches it"""

    if req.method != "GET" or not "HTTP_REFERER" in req.META:
        return HttpResponse()
    
    if kiwioptions.RESTRICT_FETCH_REFERERS:        
        if not hostrestrictions.is_valid_host_url(req.META["HTTP_REFERER"]):
            return HttpResponse()
 
    if "url" not in params:
        return HttpResponse()
    url = params["url"]
    
    if "%" in url:
        try:
            url = url % params
        except:
            pass

    if url.startswith("https://"):
        return HttpResponse()
    if not url.startswith("http://"):
        url = "http://" + url
        
    nSeconds = 3600
    if "time" in params:
        try:
            nSeconds = int(params["time"])
        except:
            pass

    result = cachedfetch.fetch(url, time=nSeconds)
    return HttpResponse(result)

