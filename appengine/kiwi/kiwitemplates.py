# Kiwi Templates

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

import os, logging

from google.appengine.api import users

import django.conf.urls
from django import shortcuts
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.template import Template, RequestContext, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

import kiwioptions
import kiwihandlers
import kiwimarkup
import kiwiauth
import cache
import cachedfetch
import rx
import hostrestrictions
import mobile
import signatures

def setupURLs(urlpatterns):
    urlpatterns += kiwiurlpatterns

def get_template(fullname, suffixes):    
    for suffix in suffixes:
        try:
            filepath = fullname + suffix
            
            if os.path.isfile(filepath):
                return filepath
        except:
            pass
        
    return None

def find_template(dir, filename):
    if filename.startswith("/"):
        filename = filename[1:]
        suffixes = kiwioptions.WEB_DEFAULT_FILE_LIST
    else:
        suffixes = kiwioptions.WEB_SUFFIXES_LIST

    fullname = os.path.join(dir, filename)
    fullname = fullname.replace('\\', '/')

    if fullname.endswith("/"):
        filepath = get_template(fullname, kiwioptions.WEB_DEFAULT_FILE_LIST)
    else:
        filepath = get_template(fullname, kiwioptions.WEB_SUFFIXES_LIST)
        if filepath:
            return filepath
        filepath = get_template(fullname + "/", kiwioptions.WEB_DEFAULT_FILE_LIST)

    return filepath

def render_template_to_response(request, templateName, responseType=HttpResponse, allowDefaultTemplates=False, allowRetry=True, args=None):
    """Renders a specified template to a string, using the specified response type
    (which gets overriden for errors and automatic permanent redirects).
    
    If allowDefaultTemplates is True, allows the default templates built into Kiwi to be found.
    
    Returns a 404 response if the template requested does not exist or the name is illegally formed.
    """
    
    if args == None:
        args = request.args

    filepath = cache.get(templateName, namespace="kiwi.t")
    fromCache = False
    
    if filepath == "":
        # We cached the fact that the file didn't exist
        filepath = None
    elif filepath:
        fromCache = True
    else:
        templateDir = kiwioptions.webDirectoryPath(request)
        filepath = find_template(templateDir, templateName)
        
        if not filepath and allowDefaultTemplates:
            filepath = find_template(kiwioptions.KIWI_TEMPLATES_PATH, templateName)
            
        if filepath:
            cache.set(templateName, filepath, 300, namespace="kiwi.t")
        else:
            cache.set(templateName, "", 60, namespace="kiwi.t")
           
    if not filepath:
        return error404(request)

    # If we get a HEAD request for a page that we'll be rendering automatically, accept it and render it as empty
    if request.method == "HEAD":
        return responseType()

    try:
        # BOGUS consider caching the contents of the file
        f = open(filepath)
        contents = f.read()
        f.close()
        
        # We differentiate Kiwi markup files by a suffix (normally .kiwi)
        if filepath.endswith(kiwioptions.WEB_MARKUP_SUFFIX):
            args["IS_KIWI_MARKUP"] = True
            s = kiwimarkup.render(request, contents, args)         # BOGUS: Cache result
            return responseType(s)
        
        # A Django template file must begin with "{". If no directive is needed, a {# Django #} comment can be used.
        if contents == "" or contents[0] != "{":
            return responseType(contents)
        
        if "{~" in contents:
            # Handle {~ auth ~} and {~ admin ~}
            contents = contents.replace("{~ admin ~}", "")

        args["IS_DJANGO"] = True

        t = Template(contents)                  # BOGUS: Cache this instead of just the pathname
        c = RequestContext(request, args)
        s = t.render(c)
        response = responseType(s)
        return response
        
    except Exception, ex:
        if fromCache:
            # Cache error can be caused by filename changing when app is updated
            # Call ourselves recursively after deleting the cache entry
            cache.delete(templateName, namespace="kiwi.t")
            return render_template_to_response(request, templateName, responseType=responseType,
                                               allowDefaultTemplates=allowDefaultTemplates, allowRetry=False, args=args)
        else:
            return error500(request)

def error403(request):
    """403 (Forbidden) handler for unauthorized pages - call this or put it in urls.py for unauthorized URLs"""

    return render_template_to_response(request, "403", responseType=HttpResponseForbidden, allowDefaultTemplates=True)

def error404(request):
    """404 handler for nonexistent pages"""

    if kiwioptions.MISSING_PAGES_REDIRECT_TO:
        return HttpResponseRedirect(kiwioptions.MISSING_PAGES_REDIRECT_TO)
    elif kiwioptions.MISSING_PAGES_REDIRECT_HOME:
        return HttpResponseRedirect("/")
    else:
        return render_template_to_response(request, "404", responseType=HttpResponseNotFound, allowDefaultTemplates=True)

def error500(request):
    """500 (Internal server error) handler for server error page"""

    return render_template_to_response(request, "500", responseType=HttpResponseForbidden, allowDefaultTemplates=True)


kiwiPathMatcher = "kiwi.pathMatcher"

def default_handler(request):
    """Default handler for Django and html pages"""

    if not rx.exists(kiwiPathMatcher):
        rx.define(kiwiPathMatcher, r"^(/)?(?P<name>.+?)(?P<suffix>(%s)%s)$" % (kiwioptions.WEB_ALLOWED_SUFFIXES, "?" if kiwioptions.WEB_PREFERRED_SUFFIX == "" else ""))

    # Separate the path into a name and suffix
    path = request.path.replace("\\", "/")
    m = rx.match(kiwiPathMatcher, path)
    if m is None:
        return error404(request)

    templateName = m.group("name")
    givenSuffix = m.group("suffix")

    # For GET requests when there is a preferred suffix, do a 301 to it if necessary
    if kiwioptions.WEB_PREFERRED_SUFFIX is not None and (request.method == "GET") and (givenSuffix != kiwioptions.WEB_PREFERRED_SUFFIX):
        newPath = "/" + templateName + kiwioptions.WEB_PREFERRED_SUFFIX
        return HttpResponsePermanentRedirect(newPath)
    
    # The urlpatterns should have filtered out any URLs with .'s, but make sure
    if templateName.find(".") > 0:
        return error404(request)
    
    return render_template_to_response(request, templateName)

def admin_handler(request, cmd=""):
    cmd = cmd.lower()

    # Following pages apply only to sites with authentication
    if not kiwioptions.EXTERNAL_AUTH:
        if cmd == "signin":
            return kiwiauth.signin(request)
        elif cmd == "signout":
            return kiwiauth.signout(request)
        elif cmd == "change_password":
            return kiwiauth.change_password(request)
        elif cmd == "member_admin":
            return kiwiauth.member_admin(request)
        elif cmd == "remember_login_on":
            return kiwiauth.remember_login(request, True)
        elif cmd == "remember_login_off":
            return kiwiauth.remember_login(request, False)
        elif cmd == "clear_cookies":
            return kiwiauth.clear_cookies(request)
        
    return error404(request)
 

# The urlpatterns created here are added to urls.urlpatterns in setupURLs,
# which needs to be called at the end of urls.py

# We match against legal filenames in the regular expressions.
# See documentation note on why we disallow "." and why it's ok to allow "/".
kiwiurlpatterns = []

from django.conf.urls.defaults import patterns

kiwiurlpatterns += patterns("", (r"^_(?P<cmd>.*)$", admin_handler))

for sfx in kiwioptions.WEB_ALLOWED_SUFFIXES.split("|"):
    kiwiurlpatterns += patterns("", (r"^[-_a-zA-Z0-9/]+$" + sfx + "$", default_handler))

kiwiurlpatterns += patterns("", (r"^[-_a-zA-Z0-9/]+$", default_handler))

if kiwioptions.HANDLE_HOME_PAGE:
    kiwiurlpatterns += patterns("", (r"^$", default_handler))
    
if kiwioptions.HANDLE_MISSING_PAGES:
    if kiwioptions.MISSING_PAGES_REDIRECT_HOME:
        kiwiurlpatterns += patterns("", (r"^.*$", kiwihandlers.redirect, {"url": "/"}))
    else:
        kiwiurlpatterns += patterns("", (r"^.*$", error404))


class Middleware(object):
    def process_request(self, request):
        request.args = self._default_page_args(request)
        
        if kiwioptions.completeArgs:
            kiwioptions.completeArgs(request.args)
            
        return None
        
    def _default_page_args(self, request):
        """Setup default arguments to be passed to the template, which can be added to in a view"""
    
        # Naming convention: All kiwi-supplied arguments are all-uppercase, reserving lowercase and mixed-case names for applications
        
        args = {"request": request, "kiwioptions": kiwioptions}
        args.update(kiwioptions.KIWI_ARGS)
        
        defaultArgs = kiwioptions.DEFAULT_ARGS
        if defaultArgs:
            args.update(defaultArgs)
        
        siteArgs = kiwioptions.webDefaultArgs(request)
        if siteArgs:
            args.update(siteArgs)
        
        self._process_signin(request, args)
        
        args["PRIMARY_PATH"] = request.path.split("/")[1]    # Path always begins with "/"
       
        args["ANALYTICS"] = mark_safe(kiwioptions.analytics)
        
        kiwiauth.update_auth_args(args)
        
        mb = request.get_cookie("MobileBrowser")
        if mb:
            if mb.lower() == "false":
                mb = False
            elif mb:
                mb = True
        else:
            mb = mobile.isMobileBrowser(request)
            request.set_cookie("MobileBrowser", mb)
        
        args["MOBILE_BROWSER"] = mb
        
        return args

    # Process the signin cookie
    def _process_signin(self, request, args):
        args["AUTHENTICATION"] = AuthenticationRenderer(request)
        
        if kiwioptions.SIGNIN_IS_KIWI:
            kiwiauth.check_signin(request, args)

        elif kiwioptions.SIGNIN_IS_GOOGLE:
            # NOTE: Google auth is only remembered for 24 hours
            # TODO: Add Google extended auth which remembers longer
            # ?? Support both straight GOOGLE and EXTENDED_GOOGLE?
            args["MEMBER"] = u = users.get_current_user()               # BOGUS: Lookup in Members table
            args["ADMIN"] = isAdmin = users.is_current_user_admin()

        elif kiwioptions.SIGNIN_IS_FACEBOOK:
            import kiwiauth_facebook  # BOGUS
            # BOGUS Handle this
            args["MEMBER"] = None
            args["ADMIN"] = False
            
        elif kiwioptions.SIGNIN_IS_TWITTER:
            import kiwiauth_twitter
            # BOGUS Handle this
            args["MEMBER"] = None
            args["ADMIN"] = False

        else:
            args["MEMBER"] = None
            args["ADMIN"] = False

class AuthenticationRenderer:
    """This class enables us wrap the request object and retrieve it when we render the signin block"""
    
    # BOGUS: Cache these renderings
    
    def __init__(self, request):
        self.request = request
        
    def IS_SIGNED_IN(self):
        return (True if self.request.args.get("MEMBER_DISPLAY_NAME") else False)

    def IS_ADMIN(self):
        return (True if self.request.args.get("MEMBER_DISPLAY_NAME") and self.request.args.get("ADMIN") else False)

    # Use INLINE_FORM for the login page
    def INLINE_FORM(self):
        if kiwioptions.SIGNIN_IS_KIWI:
            # BOGUS: Should this be moved to kiwiauth.py?

            # Set a session cookie that can be tested in the browser to see if cookies are disabled
            # This is superior to a browser-only test because it also tests if something outside
            # the browser is blocking cookies 
            self.request.set_cookie(kiwioptions.SIGNIN_COOKIE_NAME, "cookies-supported", expires=0, domain=kiwioptions.AUTH_COOKIE_DOMAIN)
            
            return render_template_to_response(self.request, "_kiwi_signin", responseType=mark_safe,
                                               allowDefaultTemplates=True, args=self.request.args)
        elif kiwioptions.SIGNIN_IS_GOOGLE:
            if self.request.args["MEMBER"]:
                signoutURL = users.create_logout_url("/")       # BOGUS: make continuePath the current page
                return "Welcome %s%s<br><br><a href='%s'>Click here to Sign Out</a>" % (
                    cgi.escape(m.nickname()), " (administrator)" if isAdmin else "", signoutURL)
            else:
                signinURL = users.create_login_url(request.path)
                return "<a href='%s'>Click here to Sign In</a>" % signinURL

    # Use LINKS for other pages on your site other than the login page
    # Can also be used for pages on other sites which share the auth cookie
    def LINKS(self):
        if kiwioptions.SIGNIN_IS_KIWI:
            # BOGUS: Move this to kiwiauth?
            return render_template_to_response(self.request, "_kiwi_welcome", responseType=mark_safe,
                                               allowDefaultTemplates=True, args=self.request.args)
        elif kiwioptions.SIGNIN_IS_GOOGLE:
            if self.request.args["MEMBER"]:
                signoutURL = users.create_logout_url("/")       # BOGUS: make continuePath the current page
                return "Welcome %s%s<br><br><a href='%s'>Click here to Sign Out</a>" % (
                    cgi.escape(m.nickname()), " (administrator)" if isAdmin else "", signoutURL)
            else:
                signinURL = users.create_login_url(request.path)
                return "<a href='%s'>Click here to Sign In</a>" % signinURL

    def EXPANDING_FORM(self):
        s = self.INLINE_FORM()
        return s    # BOGUS

    def POPUP_FORM(self):
        s = self.INLINE_FORM()
        return s    # BOGUS
    
    def SIGNIN_REQUIRED(self):
        return render_template_to_response(self.request, "_kiwi_required_signin", responseType=mark_safe,
                                           allowDefaultTemplates=True, args=self.request.args)

    def ADMIN_REQUIRED(self):
        return render_template_to_response(self.request, "_kiwi_required_admin", responseType=mark_safe,
                                           allowDefaultTemplates=True, args=self.request.args)
