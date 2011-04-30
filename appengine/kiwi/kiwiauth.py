# Signin for Kiwi

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

import logging
import datetime
import random
import cgi

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe, mark_for_escaping

from google.appengine.runtime import DeadlineExceededError

import kiwioptions
import kiwitemplates
import signatures
import strings
import stringstack

def signin(request):
    args = request.args
    
    if request.method == "POST":
        params = request.POST
    else:
        params = request.GET
    
    try:
        name = params.get("name", "")
        password = params.get("password")
        reset_password = params.get("reset_password")
        remember = params.get("remember")
        
        redirect_url = params.get("redirect_url")
        if not redirect_url:
            redirect_url = kiwioptions.SIGNIN_REDIRECT

        args["redirect_url"] = redirect_url
            
        signin_page = kiwioptions.AUTH_BASE_URL + kiwioptions.AUTH_PAGE
        
        if reset_password:
            args["signin_error_message"] = mark_safe("Reset Password is not currently enabled.<br>Please contact <a href=\"mailto:webmaster@puzzlers.org\">webmaster@puzzlers.org</a> for assistance.")
            return kiwitemplates.render_template_to_response(request, signin_page)
        
        # See if the name and password are correct
        m = kiwioptions.memberTable.get_signin_member(name, password)
        if m:
            save_signin(request, m, remember)
            m.signed_in()
            
            if m.has_temporary_password():
                return kiwitemplates.render_template_to_response(request, "_kiwi_change_password", allowDefaultTemplates=True)
            else:
                return kiwitemplates.render_template_to_response(request, "_kiwi_redirect", allowDefaultTemplates=True)
        
        # Sign in was unsuccessful. Re-render the same page with an error message
        args["signin_error_message"] = "Your signin information is incorrect. Please try again."
    
        return kiwitemplates.render_template_to_response(request, signin_page, args=args)
    
    except Exception, ex:
        args["signin_error_message"] = str(ex)
    
        return kiwitemplates.render_template_to_response(request, signin_page)
    
def change_password(request):
    args = request.args
    
    if request.method == "POST":
        params = request.POST
    else:
        params = request.GET
    
    redirect_url = params.get("redirect_url")
    if not redirect_url:
        redirect_url = kiwioptions.SIGNIN_REDIRECT

    args["redirect_url"] = redirect_url
        
    if request.method == "GET":
        return kiwitemplates.render_template_to_response(request, "_kiwi_change_password", allowDefaultTemplates=True)
    
    try:
        errs = ""

        m = args["MEMBER"]
        if not m:
            errs += "<br>You appear you have your browser's cookie functionality turned off. It must be turned on to sign into this site. "
            errs += "Click <a href=\"http://www.google.com/support/accounts/bin/answer.py?answer=61416\">here</a> for assistance in turning cookies back on."

        password = params.get("password")
        password2 = params.get("password2")
        
        minlen = kiwioptions.KIWI_PASSWORD_MINIMUM_LENGTH
        if not password or len(password) < minlen:
            errs += "<br>Password must be at least %d characters." % minlen
        if password != password2:
            errs += "<br>The two password fields must match."

        if errs:
            args["password_error_message"] = mark_safe(errs)
            return kiwitemplates.render_template_to_response(request, "_kiwi_change_password", allowDefaultTemplates=True)

        m.change_password(password)
        return kiwitemplates.render_template_to_response(request, "_kiwi_redirect", allowDefaultTemplates=True)
    
    except Exception, ex:
        args["signin_error_message"] = str(ex)
        return kiwitemplates.render_template_to_response(request, "_kiwi_change_password", allowDefaultTemplates=True)

def signout(request):
    args = request.args

    delete_auth_cookie(request)

    if request.method == "POST":
        params = request.POST
    else:
        params = request.GET
    
    redirect_url = params.get("redirect_url")
    if not redirect_url:
        redirect_url = kiwioptions.SIGNOUT_REDIRECT

    args["redirect_url"] = redirect_url
    
    return kiwitemplates.render_template_to_response(request, "_kiwi_redirect", allowDefaultTemplates=True)
        
# Update auth-specific arguments
def update_auth_args(args):
    if args["PRIMARY_PATH"] == "_member_admin":
        request = args["request"]
        
        # This makes the Sign Out button on the member admin page redirect back after a successful login
        host = request.META["HTTP_HOST"]
        args["signout_redirect_url"] = "http://" + host + "/?redirect_url=http://" + host + "/_member_admin"
    
def member_admin(request):
    args = request.args
    
    if not args["ADMIN"]:
        if kiwioptions.memberTable.members_exist():
            return kiwitemplates.error404(request)
        
        # If there are no members in the database, the member_admin function works without admin authorization
        # This allows the creation of the first users in the database
        
        args["initial_setup"] = True

        args["MEMBER_NAME"] = "Initial Setup"
        args["MEMBER_DISPLAY_NAME"] = "Initial Setup"
        args["ADMIN"] = True
        
        args["form_response"] = "To set up the first user, create them here, then use the Google App Engine console to make them an administrator."
    
    if request.method == "GET":
        return kiwitemplates.render_template_to_response(request, "_kiwi_member_admin", allowDefaultTemplates=True)
    
    params = request.POST
    
    messages = []
    errors = []

    try:
        action = params.get("action")

        if action == "add":
            lines = params["members_to_add"].replace("\r", "\n").replace("\n\n", "\n").split("\n")
        
            delimiter = params.get("delimiter", ",")
            
            # If the first line is a single character, it is an override delimiter
            if len(lines[0].strip()) == 1:
                delimiter = lines[0][0]
                del lines[0]
                
            messages.append("Delimiter is " + delimiter)
        
            for line in lines:
                if not line.strip():
                    continue

                name = "?"
                try:
                    pieces = line.split(delimiter)
                    while len(pieces) < 4:
                        pieces.append("")
                    
                    name, fullname, email, id = pieces[:5]
                        
                    if not name:
                        errors.append("Missing name in line: %s" % (line))
                        continue
                    
                    if not fullname:
                        fullname = cgi.escape(name)     # BOGUS: Deal with kiwioptions.FULLNAME_IS_HTML?
                        
                    if not email: email = None                      # Empty string isn't allowed for an email address
        
                    password = "t%06d" % random.randint(100000, 999999)
                    
                    errmsg = kiwioptions.memberTable.create_member(id, name, fullname, password, email, active=True, admin=False, temp_password=True) 
                    if errmsg:
                        errors.append("Can't create %s: %s" % (name, errmsg)) 
                    else:
                        messages.append("Added %s, temp password=%s " % (name, password))
                        
                except DeadlineExceededError, ex:
                    errors.append("<b>[Out of time, resubmit starting with %s]</b>" % (name))
                    break
        
                except errors, ex:
                    errors.append("%s got error: %s" % (name, str(ex)))
        
        else:
            # All actions other than add take a name

            name = params.get("name")
            m = kiwioptions.memberTable.get_member_from_name(name, inactive_ok=True)
            if not m:
                errors.append("The member <b>%s</b> does not exist" % (name))
            else:
                if action == "view":
                    htmlname = mark_for_escaping("%s" % m.fullname)      # BOGUS: Deal with kiwioptions.FULLNAME_IS_HTML?
                                                                         # If HTML, show raw format too
                    
                    mview = "<table><col width=150>"
                    mview += "<tr><td><b>Unique ID</b></td><td>%s</td></tr>" % (m.id)
                    mview += "<tr><td><b>%s</b></td><td>%s</td></tr>" % (kiwioptions.MEMBER_REFERENCE, m.name)
                    mview += "<tr><td><b>%s</b></td><td>%s</td></tr>" % (kiwioptions.FULLNAME_REFERENCE, m.fullname)
                    # mview += "<tr><td><b>%s</b></td><td>%s</td></tr>" % ("", htmlname)      # BOGUS: Assumption for non-NPL
                    mview += "<tr><td><b>Password</b></td><td>%s</td></tr>" % (m.password[1:] if m.password[0] == "=" else "(set by member)")
                    mview += "<tr><td><b>Email</b></td><td>%s</td></tr>" % (m.email)
                    mview += "<tr><td><b>Active</b></td><td>%s</td></tr>" % (m.active)
                    mview += "<tr><td><b>Admin</b></td><td>%s</td></tr>" % (m.admin)
                    mview += "<tr><td><b>Last Signin</b></td><td>%s</td></tr>" % (m.lastsignin)
                    mview += "</table>"
                    messages.append(mview)
                    
                    args["is_inactive"] = not m.active
        
                elif action == "activate":
                    m.set_active(True)
                    messages.append("<b>%s</b> activated" % (name))
                    
                elif action == "deactivate":
                    m.set_active(False)
                    messages.append("<b>%s</b> deactivated" % (name))
                    
                elif action == "set_temp_password":
                    pw = params.get("temppassword")
                    if (len(pw) < kiwioptions.KIWI_PASSWORD_MINIMUM_LENGTH):
                        errors.append("Password must be at least 6 characters long") 
                    else:
                        m.change_password(pw, temp_password=True)
                        messages.append("Temporary password for <b>%s</b> set to <b>%s</b>" % (name, pw))
                    
                elif action == "change_name":
                    newname = params.get("newname")
                    newfullname = params.get("newfullname")
                    if not newfullname:
                        newfullname = newname
                    m.change_name(newname, newfullname)
                    messages.append("<b>%s</b> renamed to <b>%s</b> (<b>%s</b>)" % (name, newname, newfullname))
        
                elif action == "change_email":
                    newemail = params.get("newemail")
                    m.change_email(newemail)
                    messages.append("Email for <b>%s</b> set to <b>%s</b>" % (name, newemail))
                            
                else:
                    errors.append("Unrecognized action: %s" % (action))

    except Exception, ex:
        errors.append("Exception: %s" % (str(ex)))

    response = "<span style='color:red'>Illegal operation</span><br>%s"

    response = "<br>".join(messages)
    if errors:
        response = "<span style='color:red'>%s</span><br>%s" % ("<br>".join(errors), response)
            
    args["form_response"] = mark_safe(response)

    return kiwitemplates.render_template_to_response(request, "_kiwi_member_admin", allowDefaultTemplates=True)

def remember_login(request, flag):
    # This is an admin only feature but it's actually  just hidden.
    # You can implement it as a user feature if you want.
    # BOGUS: Consider whether to change this
    set_remember_login(request, flag)
    return HttpResponse("<h2>The Remember Me option has been turned <b>%s</b> for this browser.</h2>" % ("On" if flag else "Off"))

def clear_cookies(request):
    # BOGUS: Consider whether to expose this publicly
    delete_auth_cookie(request)
    set_remember_login(request, None)
    request.delete_cookie(kiwioptions.SIGNIN_COOKIE_NAME, domain=kiwioptions.AUTH_COOKIE_DOMAIN)
    return HttpResponse("<h2>Cookies Cleared</h2><p><a href=\"/\">Sign In again</a></p>")

def delete_auth_cookie(request):
    request.delete_cookie(kiwioptions.AUTH_COOKIE_NAME, domain=kiwioptions.AUTH_COOKIE_DOMAIN)


time_stamp_format = "%a, %d-%b-%Y %H:%M:%S GMT"

def check_signin(request, args, authcookie=None):
    args["MEMBER"] = None
    args["MEMBER_NAME"] = None
    args["MEMBER_DISPLAY_NAME"] = None
    args["ADMIN"] = False
    args["UNIQUE_ID"] = None
    
    try:
        args["REMEMBER_LOGIN"] = get_remember_login(request)

        if not authcookie:
            authcookie = request.get_cookie(kiwioptions.AUTH_COOKIE_NAME)
        if authcookie:
            auth = signatures.unsign(authcookie)        # If the cookie is not valid, unsign returns None
            if auth:
                if stringstack.count(auth) == 4:  # OLD FORMAT -  BOGUS REMOVE IN JULY
                    name, display_name, flags, timestamp = stringstack.popAll(auth)
                    unique_id = None
                else:
                    unique_id, name, display_name, flags, timestamp = stringstack.popAll(auth)
                    if "\r" in unique_id or "\n" in unique_id: # BOGUS REMOVE IN JULY
                        unique_id = None

                if not kiwioptions.EXTERNAL_AUTH:
                    args["MEMBER"] = kiwioptions.memberTable.get_member_from_name(name)
                    if not args["MEMBER"]:
                        # If we're not using external auth and this member doesn't exist, we delete the authentication
                        delete_auth_cookie(request)
                        return
                    
                    # See if the cookie was created before the member changed their name or password
                    # If so, we invalidate the cookie
                    if False: # BOGUS: Finish this check
                        cd = args["MEMBER"].changeddate
                        if cd:
                            cookietime = datetime.datetime.strptime(timestamp, time_stamp_format)
                            if cd > cookietime:
                                delete_auth_cookie(request)
                                return

                    if not unique_id: # remove at some point BOGUS REMOVE IN JULY
                        # If there's no unique_id in the cookie, it's the old format. Refresh it.
                        # If we're refreshing the cookie, then it must have been remembered
                        save_auth_cookie(request, args, args["MEMBER"], True)
                    
                elif not unique_id: # remove at some point BOGUS REMOVE IN JULY
                    unique_id = name

                args["MEMBER_NAME"] = name
                args["MEMBER_DISPLAY_NAME"] = mark_safe(display_name)       # BOGUS: Deal with kiwioptions.FULLNAME_IS_HTML?
                args["ADMIN"] = "admin" in flags
                args["UNIQUE_ID"] = unique_id

    except Exception, ex:
        args["MEMBER"] = None
        args["MEMBER_NAME"] = None
        args["MEMBER_DISPLAY_NAME"] = None
        args["ADMIN"] = False
        args["UNIQUE_ID"] = None

        delete_auth_cookie(request)
        
    
def save_auth_cookie(request, args, m, remember):
    if m:
        flags = ("admin" if m.admin else "")
        timestamp = datetime.datetime.utcnow().strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        
        zid = m.id.replace("\r","").replace("\n","")
        authcookie = stringstack.push(None, zid, m.name, m.display_name(), flags, timestamp)
        
        ## BOGUS REMOVE IN JULY (left here for possible testing)
        ##authcookie = stringstack.push(None, m.id, m.name, m.display_name(), flags, timestamp)

        authcookie = signatures.sign(authcookie)
    else:
        authcookie = None
        
    if remember:
        expiration = None   # Permanent cookie
    else:
        expiration = 0      # Session cookie

    request.set_cookie(kiwioptions.AUTH_COOKIE_NAME, authcookie, expires=expiration, domain=kiwioptions.AUTH_COOKIE_DOMAIN)
    
    return authcookie

def save_signin(request, m, remember):
    authcookie = save_auth_cookie(request, request.args, m, remember)
    
    # Set args values properly
    check_signin(request, request.args, authcookie)

def set_remember_login(request, flag):
    if (flag == None):
        request.delete_cookie(kiwioptions.REMEMBER_COOKIE_NAME, domain=kiwioptions.AUTH_COOKIE_DOMAIN)
    else:
        request.set_cookie(kiwioptions.REMEMBER_COOKIE_NAME, "True" if flag else "False", domain=kiwioptions.AUTH_COOKIE_DOMAIN)
    
def get_remember_login(request):
    remembercookie = request.get_cookie(kiwioptions.REMEMBER_COOKIE_NAME)

    if not remembercookie:
        return kiwioptions.REMEMBER_LOGIN
    
    return (remembercookie == "True")
