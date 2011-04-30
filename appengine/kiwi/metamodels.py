# Kiwi meta data models, used to define other classes

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

import datetime
import pickle

from google.appengine.api import users
from google.appengine.ext import db

import cache
import codes
import kiwiproperties


# StringProperty values are limited to 500 bytes and are indexed so they take up more space in the data store
# TextProperty values are more efficient at all sizes if the index is not necessary

# META MODELS


class Cached(db.Model):
    """Inherit from this model to have the model automatically cached.
    Cached and EncodableKey are compatible with each other and may be
    specified in either order, but both must come right before db.Model
    """
    
    # Note: Can't use auto_current_user because we want control over when it's updated
    lastSaveUser = db.UserProperty()

    # Note: Can't use auto_now because we want control over when it's updated
    lastSaveTime = db.DateTimeProperty(default=None)

    @classmethod
    def get(cls, key):
        """Loads a model object, possibly from the cache"""
        
        if not key: return None
        cacheKey = "%s.%s" % (cls, key)
        result = cache.get(cacheKey)
        if not result:
            x = super(cls)
            #result = super(cls).get(key)
            result = db.Model.get(key)
        return result

    @classmethod
    # BOGUS: NEEDS A MATCHING SAVE ON PUT
    def getFromProperty(cls, prop, value):
        clsname = cls.__name__
        key = "%s.%s=%s" % (clsname, prop, value)
        result = cache.get(key)
        if result:
            return result

        q = db.GqlQuery("SELECT * FROM %s WHERE %s = :v" % (clsname, prop), v=value)
        objects = q.fetch(1)
        if len(objects) >= 1:
            result = objects[0]
            cache.set(key, result)
            return result
        
        cache.set(key, result)
        return None
 
    def putNonUserChange(self):
        """Saves a non-user change to a model object and updates the cache"""
        
        # Note: This calls db.Model, not super() to avoid an infinite recursion
        # Because of this, Cached MUST be specified right before db.Model in the ancestor class list
        
        db.Model.put(self)
        cacheKey = "%s.%s" % (self.__class__, self.key())
        cache.set(cacheKey, self)        
        
    def put(self):
        """Saves a model object, marking it as updated, and updates the cache"""
        
        self.lastSaveUser = users.get_current_user()
        self.lastSaveTime = datetime.datetime.now()
        self.putNonUserChange()
        
    @classmethod
    def refresh(cls, obj):
        """Refreshes a model object by reading it from the database again"""

        if (not obj.is_saved()): return obj
        
        k = obj.key()
        obj.uncache()
        obj = Cached.get(k)
        return obj

    def uncache(self):
        """Remove the model from the cache so that a subsequent get will re-retrieve the data from the database"""
        
        cacheKey = "%s.%s" % (self.__class__, self.key())
        cache.delete(cacheKey)


class EncodableKey(db.Model):
    """Inherit from this model to have a model with encodable keys,
    useful to prevent key guessing when keys are exposed publicly.
    Cached and EncodableKey are compatible with each other and may be
    specified in either order, but both must come right before db.Model
    """

    secretCode = kiwiproperties.SecretCodeProperty()
        
    def encodedKey(self):
        return codes.encode_key(self)

    @classmethod
    def getFromEncodedKey(cls, encodedKey):
        key, code = codes.decode_key(encodedKey)
        try:
            obj = cls.get(key)
            if obj.secretCode != code: return None
        except:
            return None

        return obj