# Memcache wrapper allows caching to be turned on and off easily.

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

"""
Version of memcache that can be disabled on the fly

When disabled, acts as if items go into the cache properly and are immediately flushed.
Disabling is useful for testing if you have a caching problem as well as for verifying
that your code works properly when the cache gets flushed unexpectedly.
"""

from google.appengine.api import memcache

import kiwioptions

# Default caching:
enabled = True
try:
    enabled = kiwioptions.CACHE
except:
    pass

def enable(*ignored):
    enabled = True
    memcache.flush_all()
    return "cache enabled"

def disable(*ignored):
    enabled = False
    return "cache disabled"

# Wrapper functions

def set(key, value, time=0, min_compress_len=0, namespace=None):
    if enabled: return memcache.set(key, value, time, namespace=namespace)
    return True

def set_multi(mapping, time=0, key_prefix='', min_compress_len=0, namespace=None):
    if enabled: return memcache.set(mapping, time, key_prefix, namespace=namespace)
    return []

def get(key, namespace=None, default=None):
    if enabled: return memcache.get(key, namespace=namespace)
    return default

def get_multi(keys, key_prefix='', namespace=None, default=None):
    if enabled: return memcache.get_multi(keys, key_prefix, namespace=namespace)
    if default is None: return {}
    return default

def delete(key, seconds=0, namespace=None):
    if enabled: return memcache.delete(key, seconds, namespace=namespace)
    return True

def delete_multi(keys, seconds=0, key_prefix='', namespace=None):
    if enabled: return memcache.delete_multi(keys, seconds, key_prefix, namespace=namespace)
    return True

def add(key, value, time=0, min_compress_len=0, namespace=None):
    if enabled: return memcache.add(key, value, time, namespace=namespace)
    return True

def add_multi(mapping, time=0, key_prefix='', min_compress_len=0, namespace=None):
    if enabled: return memcache.add_multi(mapping, time, key_prefix, namespace=namespace)
    return []

def replace(key, value, time=0, min_compress_len=0, namespace=None):
    if enabled: return memcache.replace(key, value, time, namespace=namespace)
    return False

def replace(key, value, time=0, min_compress_len=0, namespace=None):
    if enabled: return memcache.replace(key, value, time, namespace=namespace)
    return False

def replace_multi(mapping, time=0, key_prefix='', min_compress_len=0, namespace=None):
    if enabled: return memcache.replace_multi(mapping, time, key_prefix, namespace=namespace)
    return mapping.keys()
    
def incr(key, delta=1, namespace=None):
    if enabled: return memcache.incr(key, delta, namespace=namespace)
    return None

def decr(key, delta=1, namespace=None):
    if enabled: return memcache.decr(key, delta, namespace=namespace)
    return None

def flush_all():
    if enabled: return memcache.flush_all()
    return True

def get_stats():
    if enabled: return memcache.get_stats()
    return {
            "hits": 0,
            "misses": 0,
            "byte_hits": 0,
            "items": 0,
            "bytes": 0,
            "oldest_item_age": None,
            }

def disconnect_all():
    pass

def set_servers(*params):
    pass
