# Kiwi mobile browser support

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

# BOGUS Finish this for kiwi

import re

import rx

#
# MOBILE BROWSER FUNCTIONS
#

# This list is derived from the list at http://www.brainhandles.com/2007/10/15/detecting-mobile-browsers/
# Changes:
#    1) Converted to lower case
#    2) Escapes for / and . removed (incorrect for string.find)
#    3) Reordered to put more significant agent strings first. Since the list is checked in order,
#       this allows earlier agent strings to be more reliably returned than later ones.
#

__mobileBrowserAgentStrings = [
                             "blackberry", "palmos", "palmsource", "symbian", "windows ce",
                             
                             "midp", "j2me", "avantg", "docomo", "novarra", "240x320",
                             "opwv", "chtml", "pda", "mmp/", "mib/", 
                             "wireless", "nokia", "hand", "mobi", "phone", "cdm", "up.b", "audio", "sie-",
                             "sec-", "samsung", "htc", "mot-", "mitsu", "sagem", "sony", "alcatel", "lg",
                             "erics", "vx", "nec", "philips", "mmm", "xx", "panasonic", "sharp", "wap", "sch",
                             "rover", "pocket", "benq", "java", "pt", "pg", "vox", "amoi", "bird", "compal",
                             "kg", "voda", "sany", "kdd", "dbt", "sendo", "sgh", "gradi", "jb", "moto",
                             ]

# Any browser strings that need a regular expression go here
__mobileBrowserAgentRegExp = r"\d\d\di"

# BOGUS: Return False, iphone, android, None

def isMobileBrowser(req, iPhone=False, wantAgent=False):
    """Detects the type of browser in use.
    
    Set iPhone to the desired value to be returned for iPhones.
    The default is that the iPhone is considered to be a non-mobile browser.
    
    Set wantAgent to True if you want the mobile agent string that was matched to be returned.
    Setting wantAgent to be true is less performant and the agent string is not always reliable anyway.
    For unknown browsers that are believed to be mobile (because the support WAP), True is returned.
    
    Returns a non-false value if the browser is a mobile browser.
    Returns False for a non-mobile browser."""
    
    meta = req.META
    
    if "HTTP_USER_AGENT" not in meta:
        return isWAPBrowser(meta)
        
    userAgent = meta["HTTP_USER_AGENT"].lower()
    
    # Special case iPhone
    if userAgent.find("iphone") != -1:
        return iPhone
    
    if (not wantAgent) and isWAPBrowser(meta):
        return True
    
    # It might seem that this would be faster with a big regular expression,
    # but it turns out that the code to find substrings is so optimized that
    # the regular expression compiler can't compete with it.
    for s in __mobileBrowserAgentStrings:
        if userAgent.find(s) != -1:
            return s

    # But we do use regular expressions for agent strings that require them
    ##if not hasattr(RegularExpressions, "mobileMatcher"):
    ##    RegularExpressions.mobileMatcher = re.compile("(?P<agent>%s)" % __mobileBrowserAgentRegExp)
    if not rx.exists("mobileMatcher"):
        rx.define("mobileMatcher", "(?P<agent>%s)" % __mobileBrowserAgentRegExp)
    
    ##m = RegularExpressions.mobileMatcher.search(userAgent)
    matches = rx.search("mobileMatcher", userAgent)
    if matches: return matches.group("agent")

    if wantAgent and isWAPBrowser(meta):
        return True

    return False

def isWAPBrowser(meta):
    if "HTTP_X_WAP_PROFILE" in meta:
        return True

    accept = meta["HTTP_ACCEPT"] if "HTTP_ACCEPT" in meta else None
    if accept and ((accept.find("wap.") != -1) or (accept.find(".wap/i") != -1)):
        return True
    
    return False
