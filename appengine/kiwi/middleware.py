# Kiwi middleware dispatching

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

import kiwioptions
import hostrestrictions
import cookies
import httppagecaching
import kiwitemplates

# To simplify installation, we have a single middleware class for all of Kiwi.
# It then dispatches to the portions of Kiwi for each of the appropriate features

middleware_modules_classes = []

if kiwioptions.VALID_HOST_NAMES_RE:
    middleware_modules_classes.append(hostrestrictions.Middleware)
middleware_modules_classes += [cookies.Middleware, httppagecaching.Middleware, kiwitemplates.Middleware]

class KiwiMiddleware(object):
    def __init__(self):
        self.middleware_modules = []
        self.process_request_handlers = []
        self.process_response_handlers = []

        # For efficiency, figure out which handlers we actually need to call in the future
        for mw in middleware_modules_classes:
            try:
                inst = mw()
                self.middleware_modules.append(inst)
                try:
                    self.process_request_handlers.append(inst.process_request)
                except:
                    pass
                try:
                    self.process_response_handlers.append(inst.process_response)
                except:
                    pass
            except:
                pass
        
        self.process_response_handlers.append(self.process_head_response)
 
        self.process_response_handlers.reverse()
        
    def process_request(self, request):
        for proc in self.process_request_handlers:
            result = proc(request)
            if result: return result
        
        return None

    def process_response(self, request, response):
        for proc in self.process_response_handlers:
            response = proc(request, response)
            
        return response
    
    @staticmethod
    def process_head_response(request, response):
        if request.method == "HEAD":
            response.content = ""
    
        return response

def context_processor(request):
    # Note: Unlike the handlers in the KiwiMiddleware class,
    # this just returns the args dictionary created by kiwitemplates
    try:
        return request.args
    except:
        # In some cases of rendering within Kiwi, the args dictionary may not exist yet
        return {}
