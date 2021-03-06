import settings
import logging
import re

from restitem import *
from django.http import HttpResponse
from google.appengine.api import urlfetch
from google.appengine.api import memcache

import simplejson

def is_invalid(obj):
    if not obj.get("source"):
        return True
    if not obj.get("title"):
        return True
    if not obj.get("description"):
        return True
    if obj.get("source") == "":
        return True
    if obj.get("title") == "":
        return True
    if obj.get("description") == "":
        return True
    if obj.get("title") == "undefined":
        return True
    
    return False

def jdata(req, **params):
    token = params["token"]
    
    try:
        if (req.method == "GET"):
            obj = memcache.get(token)
            if not obj:
                obj = RestItem.get_from_token(token)
                if obj:
                    memcache.set(token, obj)
            
            if obj:
                response = HttpResponse(obj.data)
            else:
                response = HttpResponse("{}")
            return response
        
        if (req.method == "PUT" or req.method == "POST"):
            obj = RestItem.get_from_token(token)

            try:
                body = req.raw_post_data
                
                if obj and body == obj.data:
                    data = body
                
                else:
                    json = simplejson.loads(body)
                    
                    for item in json["items"]:
                        logging.info(str(item))
                    
                    data = simplejson.JSONEncoder().encode(json)
            except Exception, ex:
                data = '{"error": true}'
            logging.info("body=" + str(body))
                
            RestItem.add_data(token=token, data=data)
            memcache.delete(token)
            
            response = HttpResponse()
            return response
    
    except Exception, ex:
        return HttpResponse('{"exception": "%s"}' % (str(ex)))
    
    return HttpResponse()

def newsession(req, **params):
    try:
        if (req.method == "GET"):
            url = "https://staging.tokbox.com/hl/session/create"
            #params = "undefined=undefined&=127.0.0.1&undefined=undefined&echo_sup_radio=true&echo_sup_radio=false&mult_radio=true&mult_radio=false&=0&mult_switch_type_radio=0&mult_switch_type_radio=1"
            params = "=127.0.0.1&echo_sup_radio=true&echo_sup_radio=false&mult_radio=true&mult_radio=false&=0&mult_switch_type_radio=0&mult_switch_type_radio=1"
            headers = {
                       "Referer": "https://staging.tokbox.com/hl/session/create",
                       "X-TB-PARTNER-AUTH": "devsecret",
                       "Content-Type": "application/x-www-form-urlencoded"
                       }

            fr = urlfetch.fetch(method="POST", url=url, payload=params, headers=headers)

            if fr.status_code == 200:
                content = fr.content.replace("\r", "").replace("\n", "")
                matches = re.search(r"session_id\>(?P<session_id>.*)\<\/session_id", content)
                session_id = matches.group("session_id")
                
                data = {"session_id": session_id}
                
                jsonstring = simplejson.JSONEncoder().encode(data)
                
                return HttpResponse(jsonstring)

            response = HttpResponse("{}")
                    
        if (req.method == "PUT" or req.method == "POST"):
            response = HttpResponse("{}")
            return response
    
    except Exception, ex:
        return HttpResponse('{"exception": "%s"}' % (str(ex)))
    
    return HttpResponse()
