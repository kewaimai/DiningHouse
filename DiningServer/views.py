from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response,get_object_or_404,redirect
from django.template import loader, Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from DiningServer.service import meal_service,user_service,order_service,time_service,weixin_service
from DiningHouse.settings import *
from DiningServer.models import *
from DiningServer.common.func import *

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from DiningServer.read_excel import startGenerator

from DiningServer.common.time_format_util import *
from uuid import uuid4
import json
import datetime,time

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
    context = meal_service.getCategoryAndList(request)
    for k,v in context.items():
        print(k,v)
    response = render(request, 'DiningServer/index.html', context)
    response.set_cookie('house_id', context['house']['house_id']) 
    
    return response

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
    # context = user_service.getMyDetailInfo('abc')

    context = user_service.getMyDetailInfo(request.COOKIES.get('user_id'))
    print(context)
    return render(request, 'DiningServer/userInfoPage.html', context)

@csrf_exempt
def modifyMyDetailInfo(request):
    """
    修改我的信息 接口
    :param request:
    :return:
    """
    time_now = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))

    if request.method == 'POST':
        # user_id  = uuid4()
        user_id = request.COOKIES.get('user_id')
        print('user_id:',user_id)
        username = request.POST.get('username','').strip()
        print('username:',username) 
        sex      = request.POST.get('sex','').strip()
        print('sex:',sex)
        birthday = datetime.datetime.strptime(request.POST.get('birthday','2016-01-01').strip(),SERVER_DATA_FORMAT)
        # birthday = request.POST.get('birthday','').strip()
        print('birthday:',birthday,type(birthday))
        phone    = request.POST.get('phone','').strip()
        print('phone:',phone)
        email    = request.POST.get('email','').strip()
        print('email:',email)
        add_time = time_now
        location = request.POST.get('location','').strip()
        print('location:',location)
        latitude = '324'
        longitude = '453'
        user_service.modifyMyDetailInfo(user_id,username,sex,birthday,phone,email,add_time,location,latitude,longitude)
        response = HttpResponseRedirect('/DiningServer/index/')
        response.set_cookie('user_id', user_id) 
        return response

    else:
        # context = user_service.getMyDetailInfo('abc')
        context = user_service.getMyDetailInfo(request.COOKIES.get('user_id'))
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
    

    # user = user_service.getMyDetailInfo('abc')
    user = user_service.getMyDetailInfo(request.COOKIES.get('user_id','abc'))
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
    bill = order_service.createOrder(request)
    time_now = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
    meals = meal_service.getMealsAndCount(request.POST)
    count = 0
    sum = 0

    buy_meals = meals['meal_list']

    # 获取sum和count
    for meal in buy_meals:
        count += int(meal['buy_count'])
        sum += int(meal['buy_count']) * float(meal['meal_price'])

        # 保存订单中的商品
        bill_meal = TblBillMeal()
        bill_meal.id = uuid4()
        bill_meal.bill_id = bill.id
        bill_meal.house_id = bill.house_id

        bill_meal.add_time = time_now
        bill_meal.buy_count = int(meal['buy_count'])
        bill_meal.meal_price = float(meal['meal_price'])
        bill_meal.save()
    
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
    spbill_create_ip = request.META.get('REMOTE_ADDR', "120.25.151.185")
    # spbill_create_ip = "120.25.151.185"
    print('spbill_create_ip:',spbill_create_ip)
    notify_url = "http://120.25.151.183/DiningServer/pay/notify/url/"

    js_params = weixin_service.genJsAPIParams(request,body,out_trade_no,total_fee,spbill_create_ip,notify_url)
    openid = js_params.get('openid','')
    response = weixin_service.callOrderAPI(body,out_trade_no,total_fee,spbill_create_ip,notify_url,openid)
    print('js_params:',js_params)
    
    context = {
            'bill':bill,
            'bill_meal':bill_meal, 
            'meals':meals, 
            'count': count, 
            'sum':sum,
            'prepay_id':response.get('prepay_id',''),
            'appId':WC_PAY_APPID,
            'nonceStr':response.get('nonce_str',''),
            'openid':js_params.get('openid',''),
            'timeStamp':js_params.get('timeStamp',''),
            'package':"prepay_id=%s" % response.get('prepay_id',''),
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
        return False
    else:
        pay_result = weixin_service.callQueryPayResult(out_trade_no)
        order_service.payOrder(request,bill_id,pay_result)
        return HttpResponseRedirect("/DiningServer/getOrders/")


def getOrders(request):
    """
    获取用户订单页面
    :param request:
    :return: 返回”我的订单页面“
    """
    user_id = request.COOKIES.get('user_id')
    user_id = '499a2418-5bd3-4785-ab14-bd7d679ee57d'
    context = order_service.getOrders(user_id, orderType = 0)
    print(type(context))
    # return render(request, 'DiningServer/myOrder.html', context)
    return render_to_response("DiningServer/myOrder.html", {'bills':context},context_instance=RequestContext(request))

def ensureSend(request,bill_id):
    """
    确认送达 接口
    :param request:
    :return:
    """
    if order_service.ensureSend(bill_id):
        return json_response('评价成功')
    else:
        return json_response('评价失败')

@csrf_exempt
@require_POST
def getOrdersByType(request,user_id):
    """
    获取用户订单
    :param request: httprequest
    :return: 渲染后的订单列表
    """
    
    print(request.POST)
    orderType = request.POST.get('type','0')

    if int(orderType) == 0:
        context = order_service.getOrders(user_id)
    else:
        context = order_service.getOrders(user_id, int(orderType))

    return render(request, 'DiningServer/orders.html', context)


from wechat_sdk.basic import WechatBasic
from django.http.response import HttpResponseBadRequest
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import LocationMessage
from wechat_sdk.context.framework.django import DatabaseContextStore

@csrf_exempt
def getToken(request):
    token = 'szjiajia'
    wechat = WechatBasic(token=token)  
    print('request.GET:',request.GET)

    if wechat.check_signature(signature=request.GET.get('signature',''),
                              timestamp=request.GET.get('timestamp',''),
                              nonce=request.GET.get('nonce','')):
        print('echostr:',request.GET.get('echostr', 'error'))
        if request.method == 'GET':
            rsp = request.GET.get('echostr', 'error')
        else:
            print('request.body:',request.body)
            try:
                xml2dict = wechat.parse_data(request.body)
            except ParseError:
                return HttpResponseBadRequest('Invalid XML Data')

            for k,v in xml2dict.items():
                print(k,v)

            if xml2dict['Event'] == 'LOCATION':
                user = TblUser.objects.create(
                    id=uuid4(),
                    latitude=xml2dict['Latitude'],
                    longitude=xml2dict['Longitude'],
                    )
    else:
        return HttpResponseBadRequest('Verify Failed')

    response = HttpResponseRedirect('/DiningServer/index/')

    try:
        response.set_cookie('user_id', user.id)
        response.set_cookie('latitude',user.latitude)
        response.set_cookie('longitude', user.longitude)
    except:
        return HttpResponse('获取用户地理位置信息失败')

    return response


@csrf_exempt
def getPrepayid(request):
    
    print(request.POST)

    if request.method == 'POST': 
        prepay_id = request.POST.get('prepay_id', 'error')
        code_url  = request.POST.get('prepay_id', 'error')

        # bill = TblBill.objects.filter(id=bill.id).update(
        #     prepay_id=prepay_id,
        #     code_url =code_url,
        #     )
    else:
        pass

    return HttpResponse('hello')