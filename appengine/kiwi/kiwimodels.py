# Kiwi data models

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

import logging
import datetime
from hashlib import sha1

from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext import db

import cache
import codes
import metamodels
import kiwiproperties
import kiwioptions
import codes
import strings


class Member(db.Model):
    """Member of the site"""
    
    id = db.StringProperty()                                # Unique ID
    googleUser = db.UserProperty()                          # If associated with a GoogleID
    lookupname = db.StringProperty()                        # Normalized name of user, for lookup purposes
    name = db.StringProperty()                              # Signin name of this user
    oldname = db.StringProperty(default=None)               # Previous sign-in name of this user, so we can can rehash passwords on name changes
    fullname = db.StringProperty(default=None)              # Display name of this user (may not be unique)
    password = db.StringProperty()                          # Hashed password for this user
    email = db.EmailProperty(default=None)
    #secretquestion = db.StringProperty(default=None)
    #secretanswer = db.StringProperty(default=None)
    active = db.BooleanProperty(default=True)
    admin = db.BooleanProperty(default=False)
    lastsignin = db.DateTimeProperty(default=None)
    changeddate = db.DateTimeProperty(default=None)         # Date/time of last change that should invalidate a login (name, password, flag)
    resetkey = db.StringProperty(default=None)
    
    # Note: It is recommended that display names with special characters be converted to HTML entities
    # before they are stored. Otherwise, there may be encoding problems.
    def display_name(self):
        # BOGUS: Deal with kiwioptions.FULLNAME_IS_HTML?
        # How would this affect creation of the auth cookie?
        if self.googleUser:
            nickname = googleUser.nickname()
            if (self.name != nickname):
                self.name = nickname
                db.put()
        return self.fullname or self.name
    
    def email_address(self):
        if self.googleUser:
            newemail = googleUser.email()
            if (self.email != newemail):
                self.email = newemail
                db.put()
        return self.email
    
    def set_active(self, active):
        self.active = active
        self.changeddate = datetime.datetime.utcnow()
        self.put()
        
    def set_admin(self, admin):
        self.admin = admin
        self.changeddate = datetime.datetime.utcnow()
        self.put()
        
    def signed_in(self):
        self.lastsignin = datetime.datetime.now()
        self.put()
        
    def has_temporary_password(self):
        return self.password.startswith("=")
        
    @classmethod
    def create_member(cls, id, name, fullname, password, email, active=True, admin=False, temp_password=False,
                      secretquestion=None, secretanswer=None):
        if cls.get_member_from_name(name):
            return "Member already exists"

        if temp_password:
           # The = is so we can easily search for / identify temporary passwords; temporary passwords are case insensitive
            password = "=" + cls.normalize_password(password).lower()
        else:
            password = cls.hash(name, password)
            
        lookupname = cls.make_lookup_name(name)
        
        if id:
            id = strings.replaceany(id, kiwioptions.KIWI_ID_IGNORE_CHARS, "")
            
            if cls.get_member_from_id(id):
                return "Duplicate unique id"
        else:
            # Generate a unique numeric ID from the time that can't possibly be considered a privacy violation # BOGUS: Can still get bitten by a race condition
            d = datetime.datetime.utcnow()
            id = "%06d%d%07d" % (d.hour * d.minute * d.second, ord(name[0]), d.microsecond)
            while cls.get_member_from_id(id):
                id = str(int(id)+1)   # BOGUS: Random?

        m = Member(id=str(id), lookupname=lookupname, name=name, fullname=fullname, password=password, email=email, admin=admin, active=active)
        m.put()
        
        return None
    
    @classmethod
    def members_exist(cls):
        q = db.GqlQuery("SELECT * FROM Member")
        members = q.fetch(1)
        if len(members) >= 1:
            return True
            
        return False
    
    @classmethod
    def get_signin_member(cls, name, password):
        q = db.GqlQuery("SELECT * FROM Member WHERE lookupname = :n", n=cls.make_lookup_name(name))
        members = q.fetch(1)
        if len(members) >= 1:
            m = members[0]
            
            # Inactive members can't sign in
            if not m.active:
                return None
            
            # The password field can either be a temporary password (case-insensitive) or an encrypted one
            # m.password should already be lower case .. unless the database was edited
            if m.password.lower() == ("=" + cls.normalize_password(password).lower()) or m.password == cls.hash(name, password):
                return m
            
            # If the hash is with their old name, it means their name changed -- rehash the password now
            if m.oldname and m.password == cls.hash(m.oldname, password):
                m.password = cls.hash(m.name, password)
                m.oldname = None
                m.resetkey = None
                m.put()
                return m
        
        return None

    @classmethod
    def get_member_from_name(cls, name, inactive_ok=False):
        if not name:
            return None

        q = db.GqlQuery("SELECT * FROM Member WHERE lookupname = :n", n=cls.make_lookup_name(name))
        members = q.fetch(1)
        if len(members) >= 1:
            m = members[0]
            
            # Normally, we just ignore inactive members
            if (not m.active) and (not inactive_ok):
                return None
            
            return m
        
        return None
    
    @classmethod
    def get_member_from_id(cls, id):
        if not id:
            return None

        q = db.GqlQuery("SELECT * FROM Member WHERE id = :i", i=str(id))
        members = q.fetch(1)
        if len(members) >= 1:
            return members[0]
            
        return None
    
    def get_password_reset_key(self, secretanswer):
        """Generate and return a new key to reset the password
        Requires the correct secretanswer, if there is one
        """
        if (self.secretanswer and
            secretanswer.replaceany(name, kiwioptions.KIWI_NAME_LOOKUP_IGNORE_CHARS, "").lower() != 
            self.secretanswer.replaceany(name, kiwioptions.KIWI_NAME_LOOKUP_IGNORE_CHARS, "").lower()):
            return None
        
        self.resetkey = codes.make_random_code(10) + "." + self.name        # Add in name so no chance of duplication
        db.put()
        return self.resetkey
    
    @classmethod
    def get_member_to_reset(cls, key):
        q = db.GqlQuery("SELECT * FROM Member WHERE resetkey = :k", k=key)
        members = q.fetch(1)
        if len(members) >= 1:
            return members[0]
        
        return None
    
    def change_name(self, newname, newfullname):
        other = self.get_member_from_name(newname, True)
        if other:
            if self.make_lookup_name(newname) == self.make_lookup_name(other.name):
                # Just changing the existing name in some way
                self.name = newname
                self.fullname = newfullname
                self.put()
                return
                
            raise Exception("There is already a member with that %s" % (kiwioptions.MEMBER_REFERENCE.lower()))
        
        # Since the password hash uses the name, we need to save the old name in order to verify their signin.
        # Once they signin successfully, we rehash their password for subsequen tlogins.
        # Note: If we already have an oldname, this is a second name change between signins, so we ignore it.
        
        if not self.oldname:
            self.oldname = self.name
        self.lookupname = self.make_lookup_name(newname)
        self.name = newname
        self.fullname = newfullname
        self.changeddate = datetime.datetime.utcnow()
        self.put()
    
    def change_password(self, newpassword, temp_password=False):
        if temp_password:
           # The = is so we can easily search for / identify temporary passwords; temporary passwords are case insensitive
            self.password = "=" + self.normalize_password(newpassword).lower()
        else:
            self.password = self.hash(self.name, newpassword)

        self.resetkey = None
        self.changeddate = datetime.datetime.utcnow()
        self.put()
        
    def change_email(self, newemail):
        self.email = newemail
        self.put()
    
    @classmethod
    def make_lookup_name(cls, name):
        # When we look up a name, we normally ignore whitespace and case
        # The actual set of ignored characters is customizable (e.g., to ignore "." like Gmail does)
        return strings.replaceany(name, kiwioptions.KIWI_NAME_LOOKUP_IGNORE_CHARS, "").lower()
    
    @classmethod
    def normalize_password(cls, password):
        # Passwords ignore leading and trailing whitespace
        return password.strip()
    
    @classmethod
    def hash(cls, name, password):
        if not name or not password:
            return ""
        return sha1(cls.make_lookup_name(name) + cls.normalize_password(password) + kiwioptions.PASSWORD_SALT).hexdigest();
    


def equal(m1, m2):
    """Tests if two instances point to the same object in the database.
    This is needed because the GAE data store API can return different
    nstances at different times for the same data item. Note that this
    function does NOT check if the instances currently have the same values.
    """
    if m1 == m2: return True
    if (not m1) or (not m2): return False
    try:
        return m1.key() == m2.key()
    except:
        return False
