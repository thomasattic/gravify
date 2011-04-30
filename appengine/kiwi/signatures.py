# Kiwi signatures

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

import logging
import time
import datetime
from hashlib import sha1

import kiwioptions

__signOrigin = datetime.datetime(2009, 1, 1, 0, 0, 0)

def sign(what, hide=False):
	"""Signs a string with a SHA1 hash."""
	hashstr = what + kiwioptions.SIGNATURE_SALT
	hash = sha1(hashstr).hexdigest();
		
	return "%s:%s" % (hash, what)

def sign_timed(what, hours=None, minutes=0, hide=False):
	"""Signs a string and a time stamp with a SHA1 hash. Can include the string or hide it."""
	minutes += (hours * 60 if hours else 0)
	if not minutes:
		minutes = 60
	
	# Calculate the delta time from __signOrigin
	limitdelta = (datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)) - __signOrigin
	
	# timedeltas are stored as days + seconds
	result = ".%s.%s:%s" % (limitdelta.days, limitdelta.seconds, "" if hide else what)
	hashstr = ".%s.%s:%s%s" % (limitdelta.days, limitdelta.seconds, what, kiwioptions.SIGNATURE_SALT)

	hash = sha1(hashstr).hexdigest();

	return hash + result

def validate(s, what=None):
	"""Tests the validity of the signature, returning True for valid and False for invalid (see also is_invalid)."""

	return not is_invalid(s, what)

def unsign(s):
	"""Returns the original string for a signed string, or None if the signature is not valid"""

	if is_invalid(s):
		return None
	
	return s[s.find(":")+1:]
    	
def is_invalid(s, what=None):
	"""Tests the validity of a signature, returning one of:
	   False (it's valid)
	   "Expired" (it's expired, may or may not be valid otherwise)
	   "Unauthorized" (it's invalid, specific reason is not supplied)
	""" 
	try:
		if ":" not in s:
			return "Unauthorized"
	
		hash, value = s.split(":", 1)
		
		if value == "":
			if what == None:
				return "Unauthorized"
			
			value = what
		elif what and value != what:
			return "Unauthorized"
	
		if "." in hash:
			# There's an expiration time present

			pieces = hash.split(".")
			if len(pieces) != 3:
				return "Unauthorized"
		
			hash, days, seconds = pieces
			
			if not days.isdigit() or not seconds.isdigit():
				return "Unauthorized"
			
			# Convert the days+seconds offset from __signOrigin back into an absolute time
			limittime = __signOrigin + datetime.timedelta(days=int(days), seconds=int(seconds))
			if limittime < datetime.datetime.utcnow():
				return "Expired"

			hashedstring = ".%s.%s:%s%s" % (days, seconds, value, kiwioptions.SIGNATURE_SALT)

		else:
			hashedstring = value + kiwioptions.SIGNATURE_SALT
			
		if sha1(hashedstring).hexdigest() != hash:
			return "Unauthorized"
		
		return False      # It's valid

	except Exception, ex:
		return "Unauthorized"

