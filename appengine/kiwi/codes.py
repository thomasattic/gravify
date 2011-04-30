# Secret codes for obfuscation of keys

"""
Part of the Kiwi Framework, a web site development framework for Google App Engine and Django

Copyright (c) 2011 by Puzzazz, Inc.

This software is covered by the copyright and license agreement in
kiwilicense.py, which can be considered to be included here by reference.
"""

"""
Random code generator.

Random codes are used in the EncodableKey meta model to prevent a successive
keys attack against Google App Engine in places where it is necessary to
expose keys to the client.

Each data record has a permanent, random secret code associated with it and this
code is combined with the App Engine key when the key is provided to the client.
The key and code are combined in a obfuscated way. When the client sends back the key,
it is only accepted if the secret code is correct. If an attacker were to manage
to separate a code from the key and guess other keys, it would not help them because
the codes are assigned randomly and they would not have the codes associated with
other keys.
"""

import random
import datetime

indexBases = ["q", "e", "N", "A", "0"]

def encode_key(obj):
    """Return an encoded (obfuscated) key for a model object. If the model does not have a secretcode field,
    a random value is used. This still provides obfuscation but does not provide verification."""
    
    key = obj.key()
    try:
        code = obj.secretCode
    except:
        code = make_random_code(6)

    # Index is 1-9 (0 doesn't work with negative indexing into strings)
    index = 1 + (ord(code[0]) % 9)              
    
    # Encode the index with a base determined from the code
    base = indexBases[ord(code[1]) % 5]
    indexChar = chr(ord(base) + index)
    
    key = str(key)
    return key[0:-index] + code + key[-index:] + indexChar

def decode_key(encodedKey):
    """Split an encoded (obfuscated) key back into a key and a secret verification code"""

    try:
        indexChar = encodedKey[-1:]
        base = "0"
        for c in indexBases:
            if indexChar >= c:
                base = c
                break

        index = ord(indexChar) - ord(base)

        encodedKey = encodedKey[:-1]
        key = encodedKey[:-(index+6)] + encodedKey[-index:]
        code = encodedKey[-(index+6):-index]
    except:
        key = None
        code = None

    return (key, code)

# No vowels and no Q to decrease the possibilities of making words and obscenities
# Random order to make calculations from dates nonobvious
randomChars = "ty9zBSTVbcs7WXlmnpN2hY8CDFvwxGdfg1jkPRZ03rHJKLM456"

def make_random_code(nChars):
    return "".join([random.choice(randomChars) for x in range(0, nChars)])

def make_random_id(d=None):
    """Make a random 10-character ID from a date (uses current date if no date is specified)"""
    
    if not d: d = datetime.date.today()
    
    return "".join(random.choice(randomChars), random.choice(randomChars), randomChars[d.year-2008],
                   random.choice(randomChars), random.choice(randomChars), randomChars[d.month+5],
                   random.choice(randomChars), random.choice(randomChars), randomChars[d.day],
                   random.choice(randomChars))

