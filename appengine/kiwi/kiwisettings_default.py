# Default Kiwi Settings File

# DO NOT CHANGE THIS FILE - Copy it and change the copy.

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

You may create your own modified version of this file without restriction.

DO NOT CHANGE THIS FILE - Copy it and change the copy.

To modify how Kiwi works, copy this file to your app directory and rename
it kiwisettings.py, then make whatever changes you want below.
You MUST remove the copyright and notice above.
"""


# At runtime, the current value of these settings should be accessed in kiwioptions,
# not kiwisettings. These values cannot be changed at runtime.

# kiwioptions also exports a number of additional values, listed here and below.
#
#    kiwioptions.ENVIRONMENT          "local", "hosted", or "unknown"
#    kiwioptions.DEBUG                True or False
#    kiwioptions.CACHE                True or False (based on settings below)
#
# By default, DEBUG is set to True if we're running on a local server and
# False if we're running on a hosted server. Change the following line to
# make it True or False all of the time.
DEBUG = None             # Change to True or False to set on or off for all servers

# Change these lines to disable memcaching in kiwi.cache
CACHE_DEBUG = True       # Cache when DEBUG is true
CACHE_HOSTED = True      # Cache when Hosted, ignoring CACHE_DEBUG

# The following settings specify the fixed portion of the web site.
# Any files in the fixed web site (including all subdirectories) are automatically
# served as content without the need for URL paths being specified or controllers
# being written. However, files within the web directory may be overridden with
# URL paths in urls.py.

# List of valid host names or a regular expression which matches all valid host names.
# None means that all host names are accepted.
# On the dev server, "localhost" and other dotless names are automatically accepted
# At runtime, kiwioptions.VALID_HOST_NAMES_RE is a regular expression matcher
VALID_HOST_NAMES = None

# Map of host names to web site options, useful if your site has more than one
# name and you want a different web directory and/or a different set of default 
# args for each name. Each dictionary key is a case-insensitive host name.
# You must map the empty string to specify the default directory for unmatched
# host names. Each dictionary value consists of a tuple with 2 values: (dir, dict).
#
# dir must be a string specify the root-based complete name of the directory containing
# the templates for that host. Directory names should not begin or end with a slash.
#
# dict is an optional dictionary of default values to be merged into the arguments
# These values can override the values in DEFAULT_ARGS.
#
# Example:
#    WEB_SITE_MAP = { "www.domain.com": ("www", None), "xyz.domain.com": ("xyz", None), "": ("www", None) }
#
# If no WEB_SITE_MAP is supplied, the default is a www directory and no extra args
WEB_SITE_MAP = None

# The following suffixes are of the files within the templates directory
# and are unrelated to the suffixes allowed from and seen by users.
# The suffixes MUST begin with "." and be different from each another.

# Suffix of Django and HTML files
# Django files are distinguished by starting with a "{". If no directive is needed
# at the beginning a {# Django #} comment should be used.
WEB_HTML_SUFFIX = ".html"

# Suffix of Kiwi markup files
# Because they are quite different from HTML files, they are distinguished by suffix
WEB_MARKUP_SUFFIX = ".kiwi"

# At runtime, WEB_SUFFIXES_LIST is a list of all accepted suffixes, in priority order

# File to be used as the default for a URL to a directory (do not supply a suffix).
# Default files for a directory may be supplied as [WEB_DEFAULT_FILE].[suffix] within the
# directory or by having a [dirname].[suffix] file adjacent to the directory.
# At runtime, WEB_DEFAULT_FILE_LIST is a list of all default filenames, in priority order.
WEB_DEFAULT_FILE = "index"

# Regexp for suffixes which are allowed on incoming URLs
# NOTE: It is not recommended that .django or .kiwi be allowed as an incoming URL
# NOTE: This regexp must not match the empty string even if that is the preferred suffix
WEB_ALLOWED_SUFFIXES  = r"/|\.html?"

# Suffix that you prefer for your URLs from the list above (or "" if no suffix is preferred)
# When a GET of a non-preferred suffix is received, a 301 redirect to the preferred
# suffix will be returned. To allow all suffixes without 301 redirects, set this to None.
# NOTE: POST requests are always processed directly without a 301.
WEB_PREFERRED_SUFFIX = ""

# If the home page is handled by a separate controller, set this to False
HANDLE_HOME_PAGE = True

# To have missing pages handled by Kiwi, set this to True (otherwise, default Django handling gets used)
HANDLE_MISSING_PAGES = True

# TO have missing pages redirect instead of getting a 404, set one of the following options
#    To redirect to the home page, set MISSING_PAGES_REDIRECT_HOME to True
#    To redirect to a specific page, set MISSING_PAGES_REDIRECT_TO to a URL
MISSING_PAGES_REDIRECT_HOME = False
MISSING_PAGES_REDIRECT_TO = None

# Set to False to allow fetch URLs which don't come from a site in VALID_HOST_NAMES
RESTRICT_FETCH_REFERERS = True

# Set to True to automatically no-cache all pages that don't have httppagecaching set
# NOTE: httppagecaching.set_cache_limit and httppagecaching.no_cache can be used to control caching
NO_CACHE_PAGES_BY_DEFAULT = False

# The fully-qualified name of a function to call when a default template is requested
# with an {% extends default %} directive in a template. This allows an application
# to switch default templates based on the path or whether a mobile browser is in use
# The definition
# should take the following form:
#    def defaultTemplate(request, mobile)
# The function can test any of the given parameters should return the name of the template to use.
# At runtime, kiwioptions.defaultTemplate is this function
DEFAULT_TEMPLATE_FUNCTION = None

# Set to the name of the default mobile template, replaces DEFAULT_TEMPLATE when
# the current browser is a mobile browser
MOBILE_TEMPLATE = None

# Set to one of the following values: "Kiwi", "Google", "Facebook", "Twitter", None
# FUTURE: Comma-separated list of one or more
# At runtime, the following boolean values are in kiwioptions:
#    SIGNIN_IS_KIWI, SIGNIN_IS_GOOGLE, SIGNIN_IS_FACEBOOK, SIGNIN_IS_TWITTER
SIGNIN_SUPPORT = None

# Characters which are ignored when matching a login name for Kiwi login.
# Note that case is automatically ignored (with default settings, "John Smith" == "johnsmith")
# WARNING: Overriding this value after you have users in your database may make some users unable to sign in
KIWI_NAME_LOOKUP_IGNORE_CHARS = [" ", "\t", "\n", "\r"]

# Characters which are disallowed in a member ID
KIWI_ID_IGNORE_CHARS = ["\t", "\n", "\r"]

# Minimum length of a Kiwi password
KIWI_PASSWORD_MINIMUM_LENGTH = 6

# Base URL for authentication URLs
AUTH_BASE_URL = "/"

# Page under Base URL for the signin form, if it's not on the home page
AUTH_PAGE = ""

# Set to True if this site gets its authentication from another Kiwi site under the same domain
# (this means it doesn't have a Member table). All sites must have the same AUTH_COOKIE_DOMAIN.
EXTERNAL_AUTH = False

# Domain for authentication if SIGNIN_IS_KIWI (e.g., ".mycompany.com")
AUTH_COOKIE_DOMAIN = None

# Name of the authentication cookie
# (It is useful to change this to facilitate local testing with multiple Kiwi projects)
AUTH_COOKIE_NAME = "authentication"

# Whether or not the "Remember Me" checkbox is checked or unchecked by default
REMEMBER_LOGIN = True

# Name of the remember cookie - if set to True, "Remember Me" is unchecked by default
REMEMBER_COOKIE_NAME = "remember"

# Name of the cookie that gets set to tell the browser cookies are supported
SIGNIN_COOKIE_NAME = "signin"

# Default locations to redirect to after a successful signin or signout
SIGNIN_REDIRECT = "/"
SIGNOUT_REDIRECT = "/"

# Set to your Google Analytics ID
# At runtime, kiwioptions.analytics is the complete analytics string
GOOGLE_ANALYTICS_ID = None

# Google AdSense ID        # TODO
GOOGLE_ADSENSE_ID = None
GOOGLE_ADMANAGER_ID = None

# Salt to use when signing. It is highly recommended that you change this if you are using
# any features that require signing.
SIGNATURE_SALT = "signature_salt"          # WARNING: You are less secure if you do not override this
PASSWORD_SALT = "password_salt"            # WARNING: You are less secure if you do not override this

# The fully-qualified name of the table to use for members.
# If changed, must be a subclass of kiwimodels.Member.
# At runtime, kiwioptions.memberTable is this class
MEMBER_TABLE = "kiwimodels.Member"

# Whether to allow self-signup or not. If this is False, members may only be created
# through the admin interface.
SELF_SIGNUP = True

# Defines how a member is referenced in short and long form (these are two separate database fields)
# Example usage: "signin" and "Name"
MEMBER_REFERENCE = "Name"
FULLNAME_REFERENCE = "Full name"

# Whether fullnames are stored in the database in HTML.
# Setting this to True allows HTML formatting in full names, but HTML is only available
# through the admin interface or code you write. When users signup, their full names
# are converted to HTML (escaped) if this flag is set
FULLNAME_IS_HTML = False

# Dictionary of values which are added into the default page arguments
# See also WEB_SITE_MAP, which allows per-site default arguments which
# can override these values
DEFAULT_ARGS = {}

# The fully-qualified name of a function to call to setup default page arguments.
# This is called after all Kiwi-supplied values are set up. The definition
# should take the following form:
#    def defaultArgs(dict)
# At runtime, kiwioptions.completeArgs is this function
COMPLETE_ARGS_FUNCTION = None

# DO NOT CHANGE THIS FILE - Copy it and change the copy.
