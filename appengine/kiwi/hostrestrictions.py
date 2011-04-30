# Middleware that supports automatic host restrictions

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""
import re

from django.http import HttpResponseForbidden
from django.template.loader import render_to_string

import kiwioptions

class Middleware(object):
    def process_request(self, request):
        if kiwioptions.VALID_HOST_NAMES_RE:
            host = request.META["HTTP_HOST"]
            if not kiwioptions.VALID_HOST_NAMES_RE.match(host):
                return kiwitemplates.error403(req)
            
        return None


def is_valid_host_url(url):
    """Helper function to determine if a given URL is valid (for example, can be used to check a referer)"""

    if not kiwioptions.validHostNames:
        return True
    
    url = url.lower()
    
    for prefix in ("http://", "https://"):
        if url.startswith(prefix):
            url = url[len(prefix):]
            break
        
    if kiwioptions.VALID_HOST_NAMES_RE.match(url):
        return True
        
    return False

