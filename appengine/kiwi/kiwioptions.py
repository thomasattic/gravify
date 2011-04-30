# Kiwi Options - this file is configured at startup from kiwisettings.py

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

import re
import os
import settings

# Kiwi requires Django 1.0 or higher:
# If you are not using the Kiwi version of main.py, add these two lines to the top:
#    from google.appengine.dist import use_library
#    use_library('django', '1.1')

import django
if django.VERSION[0] < 1:
    raise "Django 1.0 or greater required (version=%s.%s)" % (django.VERSION[0], django.VERSION[1])

# Naming conventions:
#    UPPER_CASE for values
#    camelCase for functions

try:
    from kiwisettings_default import *
except Exception, ex:
    raise "Exception in kiwisettings_default: " + type(ex).__name__ + ", " + str(ex)

try:
    from kiwisettings import *
except Exception, ex:
    raise "Exception in kiwisettings: " + type(ex).__name__ + ", " + str(ex)

# Utility functions

def _makeHostRE(v):
    """Make a domain-matching regular expression out of a list or a regular expression string.
    On the dev server, localhost and other dotless domains are included
    """
    if type(v) == list:
        vals = ["(%s)" % x.lower() for x in v]
        v = "|".join(vals)
        v = v.replace(".", r"\.")

    if ENVIRONMENT == "local":
        v = "[^.]*|(%s)" % v
    
    return re.compile("(?i)^(%s)(/|$)" % v)

def _evalue(s):
    """Take a string of the form module.name and return the value of name from module.
    Throws an error if the model class doesn't exist
    """
    if not s: return None

    module, dot, name = s.rpartition(".")
    code = "import %s\nvalue = %s.%s" % (module, module, name)
    exec(code)
    return value


# Environment variables

try:
    ENVIRONMENT = os.environ["SERVER_SOFTWARE"].lower()
    if ENVIRONMENT.startswith("dev"): ENVIRONMENT = "local"
    elif ENVIRONMENT.startswith("google apphosting"): ENVIRONMENT = "hosted"
    else: ENVIRONMENT = "unknown"
except:
    ENVIRONMENT = "unknown"

if DEBUG is None:
    DEBUG = (ENVIRONMENT == "local")

if (ENVIRONMENT == "local"):
    CACHE = CACHE_DEBUG
else:
    CACHE = CACHE_HOSTED
    
if DEBUG:
    _errors = []
    # All errors are raised at the end
    
    if WEB_SITE_MAP is not None:
        if len(WEB_SITE_MAP) < 1:
            _errors.append("WEB_SITE_MAP is empty, must contain at least a default (empty string) match")
        elif "" not in WEB_SITE_MAP:
            _errors.append("WEB_SITE_MAP must have a default (empty string) match ")
        if re.match(WEB_ALLOWED_SUFFIXES, ""):
            _errors.append("WEB_ALLOWED_SUFFIXES cannot match empty string")
    
# Calculated values

# Naming convention: All kiwi-supplied arguments are all-uppercase, reserving lowercase and mixed-case names for applications
KIWI_ARGS = { "ENVIRONMENT": ENVIRONMENT, "DEBUG": DEBUG, "SIGNIN_SUPPORT": SIGNIN_SUPPORT }

if WEB_SITE_MAP is None:
    WEB_SITE_MAP = { "": ("www", None) }

WEB_DIRECTORY_HOME = settings.dirHome
KIWI_TEMPLATES_PATH = os.path.join(WEB_DIRECTORY_HOME, "kiwi/templates")  
WEB_DIRECTORY_DEFAULT_PATH = os.path.join(WEB_DIRECTORY_HOME, WEB_SITE_MAP.get("")[0]).replace('\\', '/')
WEB_DIRECTORY_DEFAULT_ARGS = WEB_SITE_MAP.get("")[1]

if len(WEB_SITE_MAP) == 1:
    def webDirectoryPath(req):
        return WEB_DIRECTORY_DEFAULT_PATH
    def webDefaultArgs(req):
        return WEB_DIRECTORY_DEFAULT_ARGS
else:
    WEB_PATH_MAP = {}
    WEB_ARGS_MAP = {}
    for k in WEB_SITE_MAP:
        kl = k.lower()
        WEB_PATH_MAP[kl] = os.path.join(WEB_DIRECTORY_HOME, WEB_SITE_MAP[k][0]).replace('\\', '/')
        WEB_ARGS_MAP[kl] = WEB_SITE_MAP[k][1]
    def webDirectoryPath(req):
        host = req.META["HTTP_HOST"].lower()
        return WEB_PATH_MAP.get(host, WEB_DIRECTORY_DEFAULT_PATH)
    def webDefaultArgs(req):
        host = req.META["HTTP_HOST"].lower()
        return WEB_ARGS_MAP.get(host, WEB_DIRECTORY_DEFAULT_ARGS)

WEB_SUFFIXES_LIST = [WEB_HTML_SUFFIX, WEB_MARKUP_SUFFIX]
WEB_DEFAULT_FILE_LIST = [WEB_DEFAULT_FILE + x for x in WEB_SUFFIXES_LIST]

# Note: WEB_PREFERRED_SUFFIX only works properly with certain settings of settings.APPEND_SLASH. Enforce this.
if WEB_PREFERRED_SUFFIX == "/":
    settings.APPEND_SLASH = True
elif WEB_PREFERRED_SUFFIX == "":
    settings.APPEND_SLASH = False

# On Google App Engine, naked domains don't work, so we should not be asking
# Django to redirect non-www URLs to www.
settings.PREPEND_WWW = False

try:    settings.PREPEND_WWW = kiwisettings.PREPEND_WWW
except: settings.PREPEND_WWW = False

try:    VALID_HOST_NAMES_RE = _makeHostRE(kiwisettings.VALID_HOST_NAMES)
except: VALID_HOST_NAMES_RE = None

SIGNIN_IS_KIWI = (SIGNIN_SUPPORT and "kiwi" in SIGNIN_SUPPORT.lower())
SIGNIN_IS_GOOGLE = (SIGNIN_SUPPORT and "google" in SIGNIN_SUPPORT.lower())
SIGNIN_IS_FACEBOOK = (SIGNIN_SUPPORT and "facebook" in SIGNIN_SUPPORT.lower())
SIGNIN_IS_TWITTER = (SIGNIN_SUPPORT and "twitter" in SIGNIN_SUPPORT.lower())

# This will be a concatenation of all analytics strings 
analytics = ""

if GOOGLE_ANALYTICS_ID:
    googleAnalytics = """<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', '""" + GOOGLE_ANALYTICS_ID + """']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
"""
    analytics += googleAnalytics
    
memberTable = _evalue(MEMBER_TABLE)
completeArgs = _evalue(COMPLETE_ARGS_FUNCTION)
defaultTemplate = _evalue(DEFAULT_TEMPLATE_FUNCTION)

if DEBUG:
    if _errors:
        raise Exception("; ".join(_errors))  

