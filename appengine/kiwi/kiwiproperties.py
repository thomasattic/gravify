# Kiwi data model properties

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

from google.appengine.ext import db
import codes

class SecretCodeProperty(db.StringProperty):
    def default_value(self):
        return None

    def validate(self, value):
        if value is None:
            return codes.make_random_code(6)
        return value

class DictProperty(db.TextProperty):
    _setup = False
    _string = None
    _dict = None

    def __load(self):
        if _dict is None:
            if self._string:
                _dict = pickle.loads(self._string)
            else:
                _dict = {}
        
    def default_value(self):
        return None

    def validate(self, value):
        # Since you're not supposed to assign values to a DictProperty directly,
        # this should only be called once at instantiation time
        if self._setup:
            raise TypeError("DictProperty cannot be assigned to")
    
        self._setup = True
        return value

    def make_value_from_datastore(value):
        if value != _string:
            _dict = None
        _string = value
        
    def get_value_for_datastore(model_instance):
        if self._dict:
            self._string = pickle.dumps(self._dict)
        else:
            self._string = None
   
        return _string
    
    def has_key(self, key):
        """Returns true if the dict has the specified key. 
        Can be used to distinguish between a key set to None and an unset value."""
        
        self.__load()
        return key in self._dict

    def get(self, key, default=None):
        """Returns the value for a key. If the key doesn't exist, None is returned."""
        
        self.__load()
        return self._dict.get(key)
        
    def set(self, key, value=True):
        """Sets the key value; returns True if the value changed"""
        
        self.__load()
        if key in self._dict and value == self._dict[key]:
            return False

        self._dict[key] = value
        return True
    
    def update(self, E=None, **F):
        """Updates the dictionary. Can be passed a dictionary, a list of key value pairs,
        or a number of named parameters"""
        if E:
            try:
                keys = E.keys()
                for k in keys: D[k] = E[k]
            except:
                for (k, v) in E: D[k] = v
        for k in F: D[k] = F[k]

    def remove(self, key):
        """Removes the specified key from the dictionary. Returns True if the key existed."""

        self.__load()
        if key not in self._string:
            return False
        
        del self._dict[key]
        return True

    def copy(self):
        """Returns a copy of the dictionary"""
        
        self.__load()
        return self._dict.copy()
    
    def keys(self):
        """Returns a list of the keys"""
        
        self.__load()
        return self._dict.keys()
    
    def values(self):
        """Returns a list of the values"""
        
        self.__load()
        return self._dict.values()
