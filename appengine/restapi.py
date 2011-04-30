import settings

from restitem import *
from django.http import HttpResponse

def handler(req, **params):
    id = params["id"]
    
    if (req.method == "GET"):
        obj = RestItem.get_from_id(id)
        
        if obj:
            response = HttpResponse(obj.data)
        else:
            response = HttpResponse("{}")
        return response
    
    if (req.method == "POST"):
        RestItem.add_item(id=id, data=req.body)
        
        response = HttpResponse()
        return response
    
    return HttpResponse()
