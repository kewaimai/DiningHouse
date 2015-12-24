from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
import json as simplejson


def json_error_response(request,msg):
    res = dict(success=0,error_message=msg)
    return json_response(request,res)

def json_msg_response(request,msg):
    res = dict(success=1,msg_message=msg)
    return json_response(request,res)

def json_response(request,res,cookie=dict()):
    response = HttpResponse(simplejson.dumps(res))
    if cookie :
        response.set_cookie(cookie['key'],cookie['value'],expires=cookie['expires'])
    return response