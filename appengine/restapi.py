import settings

from restitem import *
from django.http import HttpResponse

def handler(req, **params):
    token = params["token"]
    
    try:
        if (req.method == "GET"):
            obj = RestItem.get_from_token(token)
            
            if obj:
                response = HttpResponse(obj.data)
            else:
                response = HttpResponse("{}")
            return response
        
        if (req.method == "PUT" or req.method == "POST"):
            try:
                body = req.raw_post_data
            except Exception, ex:
                body = '{"error": true}'
            logging.info("body=" + str(body))
                
            RestItem.add_data(token=token, data=body)
            
            response = HttpResponse()
            return response
    
    except Exception, ex:
        return HttpResponse('{"exception": "%s"}' % (str(ex)))
    
    return HttpResponse()
