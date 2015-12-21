# import httplib
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from DiningHouse.settings import *
from DiningServer.models import *

from DiningServer.common.weixin_pay.weixin_pay import UnifiedOrderPay
from DiningServer.common.weixin_pay.weixin_pay import JsAPIOrderPay
from DiningServer.common.weixin_pay.weixin_pay import OrderQuery


#调用统一下单API
def CallOrderAPI(body,out_trade_no,total_fee,spbill_create_ip,notify_url):
    pay = UnifiedOrderPay(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY)

    response = pay.post(body,out_trade_no,total_fee,spbill_create_ip,notify_url)
    if response and response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS":
        prepay_id = response["prepay_id"] #预支付ID
        code_url = response["code_url"]   #二维码链接
    else:
        print('response:\n',response)
        if response["return_code"] == "FAIL":
            err_code_des = response["return_msg"]
            #通信失败处理
        # if response["result_code"] == "FAIL":
        #     err_code = response["err_code"]
        #     err_code_des = pay.get_error_code_desc(response["err_code"])
        #     交易失败处理


#生成JSAPI页面调用的支付参数并签名
def GenerJsAPIParams(request):
    pay = JsAPIOrderPay(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY,WC_PAY_APPSECRET)

    #先判断request.GET中是否有code参数，如果没有，需要使用create_oauth_url_for_code函数获取OAuth2授权地址后重定向到该地址并取得code值
    oauth_url = pay.create_oauth_url_for_code("http://www.szjiajia.com/pay/url/")
    #重定向到oauth_url后，获得code值
    code = request.GET.get('code', None)

    if code:
        #使用code获取H5页面JsAPI所需的所有参数，类型为字典
        josn_pay_info = pay.post("body", "out_trade_no", "total_fee", "127.0.0.1", "http://www.szjiajia.com/pay/notify/url/", code)
        return josn_pay_info

#查询支付结果
def CallQueryPayResult():
    pay = OrderQuery(WC_PAY_APPID, WC_PAY_MCHID, WC_PAY_KEY)
    response = pay.post("out_trade_no")
    if response and response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS":
        trade_state = response["trade_state"]
        if trade_state == "SUCCESS": #支付成功
            return True
            #处理支付成功的情况
        else:
            pass #处理支付未完成的情况，trade_state的枚举值参见微信官方文档说明