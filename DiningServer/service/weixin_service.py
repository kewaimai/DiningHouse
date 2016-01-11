# -*- encoding=utf-8 -*- 
# import httplib
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from DiningHouse.settings import *
from DiningServer.models import *

from DiningServer.common.weixin_pay.weixin_pay import UnifiedOrderPay
from DiningServer.common.weixin_pay.weixin_pay import JsAPIOrderPay
from DiningServer.common.weixin_pay.weixin_pay import OrderQuery

import http.client, urllib

body='body'
out_trade_no='out_trade_no'
total_fee=100
spbill_create_ip='127.0.0.1'
notify_url="http://120.25.151.183/DiningServer/pay/notify/url/"

#调用统一下单API
def callOrderAPI(body,out_trade_no,total_fee,spbill_create_ip,notify_url,openid):
    
    pay = UnifiedOrderPay(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY)

    response = pay.post(body,out_trade_no,total_fee,spbill_create_ip,notify_url,openid)
    print('response:',type(response))
    for k,v in response.items():
        print(k.encode('utf-8'),v.encode('utf-8'))
    if response and response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS":
        prepay_id = response["prepay_id"] #预支付ID
        code_url = response["code_url"]   #二维码链接

        print('prepay_id,code_url:',prepay_id,code_url)

        return response
    else:
        if response["return_code"] == "FAIL":
            err_code_des = response["return_msg"]
            return
            #通信失败处理
        try:
            response["result_code"] == "FAIL"
            err_code = response["err_code"]
            err_code_des = pay.get_error_code_desc(response["err_code"])
            #交易失败处理
        except:
            pass


#生成JSAPI页面调用的支付参数并签名
def genJsAPIParams(request,ody,out_trade_no,total_fee,spbill_create_ip,notify_url):
    pay = JsAPIOrderPay(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY,WC_PAY_APPSECRET)

    #先判断request.GET中是否有code参数，如果没有，需要使用create_oauth_url_for_code函数获取OAuth2授权地址后重定向到该地址并取得code值
    
    print('request.GET(code):',request.GET)

    if 'code' not in request.GET:
        oauth_url = pay.create_oauth_url_for_code("http://120.25.151.183/DiningServer/payOrder/")
        print('oauth_ur:',oauth_url)
        redirect(oauth_url)
        print('redirect:',oauth_url)
        # requests.get(oauth_url)

    code = request.GET.get('code', None)
    print('code:',code)

    #使用code获取H5页面JsAPI所需的所有参数，类型为字典
    js_params = pay.post(body,out_trade_no,total_fee,spbill_create_ip,notify_url,code)
    return js_params

#查询支付结果
def callQueryPayResult(out_trade_no):
    pay = OrderQuery(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY)
    response = pay.post(out_trade_no)
    if response and response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS":
        trade_state = response["trade_state"]
        if trade_state == "SUCCESS": #支付成功
            return True
            #处理支付成功的情况
        else:
            return False
            #处理支付未完成的情况，trade_state的枚举值参见微信官方文档说明


def sendRequest(host, path, method, port=443, **params):
    client = http.client.HTTPSConnection(host, port)

    path = '?'.join([path, "&".join(['%s=%s'%(k, v) for k,v in params.items()])])
    client.request(method, path)
 
    res = client.getresponse()
    conn.close()
    if not res.status == 200:
        return False, res.status
    return True, json.loads(res.read())

    # httpRequest = ""
    # conn = http.client.HTTPConnection("localhost",8080)
    # conn.request("GET","/file.html",httpRequest)
    # response = conn.getresponse()
    # print(response.status,response.reason)
    # conn.close()
    
def getAccessToken():
    params = {
        'grant_type': 'client_credential',
        'appid': WC_PAY_APPID,
        'secret': WC_PAY_APPSECRET
    }
    host = 'api.weixin.qq.com'
    path = '/cgi-bin/token'
    method = 'GET'
 
    res = sendRequest(host, path, method, params=params)
    print('res:',res)
    if not res[0]:
        return False
    if res[1].get('errcode'):
        return False
    return res[1]