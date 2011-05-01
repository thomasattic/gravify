import settings
import logging
import re

from restitem import *
from django.http import HttpResponse
from google.appengine.api import urlfetch

import simplejson

def jdata(req, **params):
    token = params["token"]
    
    try:
        obj = RestItem.get_from_token(token)

        if (req.method == "GET"):    
            if obj:
                response = HttpResponse(obj.data)
            else:
                response = HttpResponse("{}")
            return response
        
        if (req.method == "PUT" or req.method == "POST"):
            try:
                body = req.raw_post_data
                
                if obj and body == obj.data:
                    data = body
                
                else:
                    json = simplejson.loads(body)
                    
                    for item in json["items"]:
                        logging.info(str(item))
                        
                        # title for new items is "newly added...", so check for description instead
                        if not item.get("source"):
                            item["source"] = "youtube"      # Hard coded

                            fr = urlfetch.fetch("http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json" % item.get("id"))
                            if fr.status_code == 200:
                                vdata = simplejson.loads(fr.content)
                                title = vdata["entry"]["title"]["$t"]
                                description = vdata["entry"]["media$group"]["media$description"]["$t"]
                                
                                item["title"] = title
                                item["description"] = description
                        
                        # Weed out duplicates
                        # Currently collisions => last ones win
                    
                    data = simplejson.JSONEncoder().encode(json)
                    
            except Exception, ex:
                data = '{"error": true}'
            logging.info("body=" + str(body))
                
            RestItem.add_data(token=token, data=data)
            
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
