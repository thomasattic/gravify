# Middleware that provides easy access to cache control in the response 

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

"""
Allows setting cache options on the Request object rather than waiting until the
Response object is created. Adds two methods to the Request object:

req.set_cache_limit(limit_string)

        Set a specific cache limit for the page
        
req.set_no_cache()

        Turn off caching for the page
"""


import kiwioptions

class Middleware(object):
    def process_request(self, request):
        # We assign additional methods to the request class every time.
        # This is faster than checking if we've already done it
        c = request.__class__
        c.set_cache_limit = set_cache_limit_method
        c.set_no_cache = set_no_cache_method
        
        request.kiwi_caching = None
        
        return None
        
    def process_response(self, request, response):
        if kiwioptions.NO_CACHE_PAGES_BY_DEFAULT:
            caching = False
        else:
            caching = request.kiwi_caching

        if caching is not None:
            if self == False:           # BOGUS - revisit this code
                try:
                    if response.has_header("cache-control"):
                        del response["cache-control"]
                    if response.has_header("Cache-Control"):
                        del response["cache-control"]
                except:
                    pass
                
                response["Cache-Control"] = "no-cache"
            else:
                response["Expires"] = caching
                    
        return response

# Instance methods added to the request object
def set_cache_limit_method(self, limit):
    self.kiwi_caching = limit
    
def set_no_cache_method(self):
    self.kiwi_caching = False
