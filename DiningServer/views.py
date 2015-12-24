from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response,get_object_or_404,redirect
from django.core.exceptions import ObjectDoesNotExist
from DiningServer.service import meal_service,user_service,order_service,time_service,weixin_service
from DiningHouse.settings import *
from DiningServer.models import *
from DiningServer.common.func import *

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from DiningServer.read_excel import startGenerator

import json
"""
在这里郑重声明   order = bill =  订单
"""

# Create your views here.

def generatorMeals(request):
    """
    调用service从excl中构造meal
    :param request:
    :return:
    """
    startGenerator()
    return HttpResponse('success hahahaha')

def indextest(request):
    """
    测试test
    :param request:
    :return:
    """
    context = meal_service.getCategoryAndList()
    print(context)
    return HttpResponse(str(context))

def index(request):
    """
    首页
    :param request:
    :return:
    """
    context = meal_service.getCategoryAndList()
    return render(request, 'DiningServer/index.html', context)

def getMealDetail(request,meal_id):
    """
    获取商品详情页面
    :param request:
    :param meal_id:
    :return:
    """
    # return HttpResponse(json.dumps(meal_service.getMealDetail('1')))
    context = meal_service.getMealDetail(meal_id)
    return render(request, 'DiningServer/details.html', context)


"""
评价订单以及获取评价等页面
"""

def getJudgeMealPage(request):
    """
    获取评价Meal页面  需要传订单id
    :param request:
    :return:
    """
    return HttpResponse('')

@require_POST
def judgeMeal(request):
    """
    评价商品
    :param request:
    :return:
    """
    # meal_service.judgeMeal()
    return HttpResponse('')

def getMealJudge(request):
    """
    获取商品评价界面
    :param request:
    :return:
    """
    return HttpResponse('')


"""
个人信息相关
"""

def getMyDetailInfoPage(request):
    """
    获取我的相信信息接口
    :param request:
    :return:
    """
    # 获取userid
    # 使用ensure_ascii = False   否则的话中文会只显示编码 不显示汉字
    context = user_service.getMyDetailInfo('abc')
    print(context)
    return render(request, 'DiningServer/userInfoPage.html', context)

def modifyMyDetailInfo(request):
    """
    修改我的信息 接口
    :param request:
    :return:
    """
    user_service.modifyMyDetailInfo('abc','mingzi','女','1998-10-11','1212312','auisa@qq.com','中关村南大街')
    context = user_service.getMyDetailInfo('abc')
    return render(request, 'DiningServer/userInfoPage.html', context)



"""
订单相关页面及接口
"""

@csrf_exempt
@require_POST
def gotoOrderPage(request):
    """
    点击去下单 跳转到的页面
    :param request:
    :return:
    """
    user = user_service.getMyDetailInfo('abc')
    meals = meal_service.getMealsAndCount(request.POST)
    count = 0
    sum = 0

    buy_meals = meals['meal_list']
    # 获取sum和count
    for meal in buy_meals:
        print('meal in buy_meal:\n',meal)
        count += int(meal['buy_count'])
        sum += int(meal['buy_count']) * float(meal['meal_price'])
    times = time_service.getTimeOption()
    context = {'meals':meals, 'user':user, 'times': times, 'count': count, 'sum':sum}
    return render(request, 'DiningServer/shopping.html', context)

# 创建订单 创建完成后自动跳转到支付页面
@csrf_exempt
@require_POST
def createOrder(request):
    """
    创建订单接口
    :param request:
    :return:
    """
    meals = meal_service.getMealsAndCount(request.POST)
    count = 0
    sum = 0

    buy_meals = meals['meal_list']

    # 获取sum和count
    for meal in buy_meals:
        count += int(meal['buy_count'])
        sum += int(meal['buy_count']) * float(meal['meal_price'])

    (bill,bill_meal) = order_service.createOrder(request)
    print("count:",count)
    print("sum:",sum)
    print("order Done!!!")
    (yuan,fen) = str('%.2f' % sum).split('.')
    print(yuan,fen)
    print(bill.id)
    print(bill.bill_content)
    body = 'jiajiamifen'
    out_trade_no = str(bill.id).replace('-','')
    total_fee = int(yuan)*100 + int(fen)
    spbill_create_ip = request.META.get('REMOTE_ADDR', "127.0.0.1")
    notify_url = "http://www.szjiajia.com/pay/notify/url/"

    response = weixin_service.callOrderAPI(body,out_trade_no,total_fee,spbill_create_ip,notify_url,bill)
    js_params = weixin_service.genJsAPIParams(request,body,out_trade_no,total_fee,spbill_create_ip,notify_url)
    print('js_params:',js_params)
    
    context = {
            'bill':bill,
            'bill_meal':bill_meal, 
            'meals':meals, 
            'count': count, 
            'sum':sum,
            'prepay_id':response.get('prepay_id',''),
            'appId':response.get('appid','wxacfdb1da76aa7763'),
            'nonceStr':response.get('nonce_str','hhxLvW9mk6hK0HO9'),
            'openid':js_params.get('openid',''),
            'timeStamp':js_params.get('timeStamp',''),
            'package':js_params.get('package',''),
            'signType':js_params.get('signType',''),
            'paySign':js_params.get('paySign',''),
            }
    return render(request, 'DiningServer/createOrder.html', context)
            
@csrf_exempt
@require_POST
def payOrder(request,bill_id):
    """
    用户支付订单接口
    :param request:
    :return:
    """
    pay_result = False
    out_trade_no = str(bill_id).replace('-','')

    try:
        bill = TblBill.objects.get(id=bill_id)
    except ObjectDoesNotExist:
        pass
    
    pay_result = weixin_service.callQueryPayResult(out_trade_no)
    order_service.payOrder(request,bill_id,pay_result)
    return HttpResponseRedirect("/getOrders/%s/" % bill_id)

def getOrders(request,bill_id):
    """
    获取用户订单页面
    :param request:
    :return: 返回”我的订单页面“
    """
    context = order_service.getOrders(user_id, orderType = 0)
    return render(request, 'DiningServer/myOrder.html', context)

def ensureSend(request):
    """
    确认送达 接口
    :param request:
    :return:
    """
    if order_service.ensureSend('1'):
        return HttpResponse('success')
    else:
        return HttpResponse('error')

@csrf_exempt
@require_POST
def getOrdersByType(request):
    """
    获取用户订单
    :param request: httprequest
    :return: 渲染后的订单列表
    """
    print(request.POST)
    if '0' in request.POST['type']:
        context = order_service.getOrders('abc')
    else:
        context = order_service.getOrders('abc', request.POST['type'])
    print(context)
    return render(request, 'DiningServer/orders.html', context)