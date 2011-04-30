# Middleware which allows cookies to be specified before a Django response object is created 

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

"""
Allows creating and deleting cookies using the Request object rather than waiting until
the Response object is created. Adds two methods to the Request object:

req.set_cookie(cookie, value, expires=None)

    The expiration time is specified in hours. A expiration time of 0 designates a session
    cookie. An expiration time of None means non-expiring (actually 10 years).
    If set_cookie is called multiple times for the same cookie, the most recent value is used.
  
req.delete_cookie(cookie)

    Deletes the specified cookie.
    
If both set_cookie and delete_cookie are called for the same cookie, the last call takes precedence.
"""

import datetime

import strings

cookie_escaped_chars = "\"'<>=;"

class Middleware(object):
    def process_request(self, request):
        # We assign additional methods to the request class every time.
        # This is faster than checking if we've already done it
        c = request.__class__
        c.get_cookie = get_cookie_method
        c.set_cookie = set_cookie_method
        c.delete_cookie = delete_cookie_method
        
        request.kiwi_cookies = {}

        return None
                
    def process_response(self, request, response):
        cr = request.kiwi_cookies

        if len(cr):
            for cookie in cr.keys():
                value, expires, domain = cr[cookie]
                
                if value:
                    value = strings.escapechars(value, cookie_escaped_chars)
                
                if domain == "base":
                    pass    # BOGUS -- calculate automatically e.g., ".puzzlers.org"
                
                if value is None:
                    response.delete_cookie(cookie, domain=domain)
                elif expires is None:
                    # Non-expiring is actually ten years
                    utc = datetime.datetime.utcnow()
                    utc += datetime.timedelta(days=3650)
                    when = utc.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
                    response.set_cookie(cookie, value, expires=when, domain=domain)
                elif expires == 0:
                    # Session cookie
                    response.set_cookie(cookie, value, domain=domain)
                else:
                    # Expire in specified number of hours
                    utc = datetime.datetime.utcnow()
                    utc += datetime.timedelta(hours=expires)
                    when = utc.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
                    response.set_cookie(cookie, value, expires=when, domain=domain)
               
        return response

  
def set_cookie_method(self, cookie, value, expires=None, domain=None):
    self.kiwi_cookies[cookie] = (value, expires, domain)
  
def delete_cookie_method(self, cookie, domain=None):
    self.set_cookie(cookie, None, domain=domain)

def get_cookie_method(self, cookie):
    c = self.kiwi_cookies.get(cookie)
    if c:
        value = c[0]
    else:
        value = self.COOKIES.get(cookie)
        
    if value:
        return strings.unescapechars(value, cookie_escaped_chars)

    return None
