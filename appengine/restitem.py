import logging
import datetime

from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext import db

from kiwi import kiwioptions

class RestItem(db.Model):
    id = db.StringProperty()
    data = db.TextProperty()
    lastchanged = db.DateTimeProperty(auto_now=True)

    @classmethod
    def get_from_id(cls, id):
        try:
            q = db.GqlQuery("SELECT * FROM RestItem WHERE id = :i", i=id)
            results = q.fetch(1)
            if len(results) >= 1:
                return results[0]
            
            return None
        except:
            return None
        
    @classmethod
    def add_data(cls, **params):
        try:
            id = params["id"]
            obj = cls.get_from_id(id)
            
            if obj:
                obj.data = params["data"]
            
            else:
                obj = RestItem(**params)
                
            obj.put()
            
            return obj
        
        except Exception, ex:
            logging.info("Exception creating RestItem: " + str(ex))
            return None
    
    @classmethod
    def remove_entry(cls, id):
        obj = cls.get_from_id(id)
        if obj:
            db.delete(obj)
        
    @classmethod
    def all_records(cls, con):
        try:
            q = db.GqlQuery("SELECT * FROM RestItem ORDER BY id")
            results = q.fetch(1000)
            return results
        except Exception, ex:
            logging.info("Exception in RestItem.all_records: " + str(ex))
            return None
