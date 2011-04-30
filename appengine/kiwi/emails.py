# Email utilities

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

import rx

def is_valid_email(e):    
    ##if not hasattr(RegularExpressions, "emailMatcher"):
    if not rx.exists("emailMatcher"):
        # See RFC 2821, RFC 2822, RFC 3696
        
        # lots of legitimate chars in localname, but can't start or end with a .
        # Not all emailers support all of these characters
        localnameChars = r"[-.a-zA-Z0-9!#$%*/?|^{}`~'""+=_]"
        localnameTerminalChars = r"[-a-zA-Z0-9!#$%*/?|^{}`~'""+=_]"
        localnameRE = r"(%s|%s%s{0,62}%s)" % (localnameTerminalChars, localnameTerminalChars, localnameChars, localnameTerminalChars)
        
        # Domain name can't start or end with a . or -
        domainChars = r"[-.a-zA-Z0-9]"
        domainTerminalChars = r"[a-zA-Z0-9]"
        hostnameRE = r"(%s|%s%s*%s)" % (domainTerminalChars, domainTerminalChars, domainChars, domainTerminalChars)
        
        tldChars = r"[a-zA-Z]"
        tldIntlChars = r"[a-zA-Z0-9]"
        tldRE = r"(%s{2,10}|\.xn--%s+)" % (tldChars, tldIntlChars)
        
        emailRE = r"^(?P<localname>%s)@(?P<hostname>%s)\.(?P<tld>%s)$" % (localnameRE, hostnameRE, tldRE)
        
        rx.define("emailMatcher", emailRE)
    
    matches = rx.match("emailMatcher", e)
    if matches is None:
        return False
    
    localname = matches.group("localname")
    hostname = matches.group("hostname")
    
    if localname.find("..") != -1 or hostname.find("..") != -1:
        return False

    return True

def parse_emails(s, emailInviteLimit=5):
    """Parses and validates a string of comma or semicolon separated emails.
    If there are any invalid emails, an error string listing them is returned.
        
    Returns (emailList, errorString)"""
    
    if s is None:
        return (None, "You must supply at least one email address")

    # Allow either commas or semicolons to separate email addresses
    unverifiedList = s.replace(";", ",").split(",")
    
    verifiedList = None
    invalidEmails = None

    for e in unverifiedList:
        e = e.strip()
        if e == "":
            continue

        if is_valid_email(e):
            if verifiedList is None:
                verifiedList = []
            verifiedList.append(e)
        else:
            if invalidEmails is None:
                invalidEmails = e
            else:
                invalidEmails += ", " + e
        
    if verifiedList is None and invalidEmails is None:
        return (None, "You must supply at least one email address")
    
    if invalidEmails is not None:
        invalidEmails = "These email addresses are invalid: " + invalidEmails
     
    elif len(verifiedList) > emailInviteLimit:
        invalidEmails = "To prevent spamming, you cannot invite more than %d people at a time" % emailInviteLimit
    
    return (verifiedList, invalidEmails)
