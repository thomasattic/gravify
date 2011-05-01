import settings
import logging

from restitem import *
from django.http import HttpResponse
from google.appengine.api import urlfetch

import simplejson

def handler(req, **params):
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
