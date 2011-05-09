import logging
import datetime

from django.http import HttpResponse

from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import memcache

from kiwi import kiwioptions

class EmailSignup(db.Model):
    email = db.StringProperty()
    count = db.IntegerProperty(default=0)
    lastchanged = db.DateTimeProperty(auto_now=True)

    @classmethod
    def get_from_email(cls, email):
        try:
            q = db.GqlQuery("SELECT * FROM EmailSignup WHERE email = :e", e=email)
            results = q.fetch(1)
            if len(results) >= 1:
                return results[0]
            
            return None
        except Exception, ex:
            return None
        
    @classmethod
    def add_email(cls, **params):
        try:
            email = params["email"]
            obj = cls.get_from_email(email)
            
            if obj:
                return obj
 
            obj = EmailSignup(**params)    
            obj.put()
            
            return obj
        
        except Exception, ex:
            logging.info("Exception creating EmailSignup: " + str(ex))
            return None
    
    @classmethod
    def decrement_email(cls, **params):
        try:
            email = params["email"]
            obj = cls.get_from_email(email)
            
            if not obj:
                obj = EmailSignup(**params)

            obj.count -= 1;
            obj.put()
            
            return obj
        
        except Exception, ex:
            logging.info("Exception decrementing EmailSignup: " + str(ex))
            return None
    
    @classmethod
    def set_count_for_email(cls, **params):
        try:
            email = params["email"]
            obj = cls.get_from_email(email)
            
            if not obj:
                obj = EmailSignup(**params)

            obj.count = int(params["newvalue"])
            obj.put()
            
            return obj
        
        except Exception, ex:
            logging.info("Exception setting count for EmailSignup: " + str(ex))
            return None
    
    @classmethod
    def remove_email(cls, email):
        obj = cls.get_from_email(email)
        if obj:
            db.delete(obj)
        
    @classmethod
    def all_records(cls, con):
        try:
            q = db.GqlQuery("SELECT * FROM EmailSignup ORDER BY email")
            results = q.fetch(1000)
            return results
        except Exception, ex:
            logging.info("Exception in EmailSignup.all_records: " + str(ex))
            return None


def handler(req, **params):
    operator = params["operator"].lower()
    email = params["email"]
    
    try:
        # We handle GET and POST the same here
        
        obj = memcache.get(email)
        if not obj:
            obj = EmailSignup.get_from_email(email)
            if obj:
                memcache.set(email, obj)
                
        if (operator == "add"):
            if obj:
                return HttpResponse('{"status": "duplicate"}')
                
            obj = EmailSignup.add_email(email=email)
            if obj:
                return HttpResponse('{"status": "added"}')
            
            return HttpResponse('{"status": "error", "error": "Unable to add email"}')
            
        if (operator == "decrement"):
            obj = EmailSignup.decrement_email(email=email)
            memcache.set(email, obj)
            if obj:
                return HttpResponse('{"status": "decremented", "count": "%d"}' % obj.count)
            
            return HttpResponse('{"status": "error", "error": "Unable to decrement email"}')
        
        if (operator == "get"):
            if obj:
                return HttpResponse('{"status": "found", "count": "%d"}' % obj.count)
            
            return HttpResponse('{"status": "error", "error": "Unable to get count for email"}')
        
        if (operator == "authorize"):
            newvalue = params["newvalue"] if ("newvalue" in params) else "3"
            obj = EmailSignup.set_count_for_email(email=email, newvalue=newvalue)
            memcache.set(email, obj)
            if obj:
                return HttpResponse('{"status": "authorized", "count": "%d"}' % obj.count)
            
            return HttpResponse('{"status": "error", "error": "Unable to authorize email"}')
        
        return HttpResponse('{"status": "error", "error": "Unknown operator: %s"}' % params["operator"])
    
    except Exception, ex:
        return HttpResponse('{"status": "error", "error": "%s"}' % (str(ex)))
