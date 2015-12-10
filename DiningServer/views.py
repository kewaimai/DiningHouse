from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from DiningServer.service import meal_service
from DiningServer.service import user_service
from DiningServer.service import order_service
from DiningServer.service import time_service
import json

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from DiningServer.read_excel import startGenerator

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
    return render(request,'DiningServer/toJudge.html',{})

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
    context = {}
    return render(request,'DiningServer/comoder.html',context)


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
    print(meals)
    buy_meals = meals['meal_list']
    print(buy_meals)
    # 获取sum和count
    for meal in buy_meals:
        print(meal)
        count += int(meal['buy_count'])
        sum += int(meal['buy_count']) * float(meal['meal_price'])
    times = time_service.getTimeOption()
    print(count, sum)
    context = {'meals':meals, 'user':user, 'times': times, 'count': count, 'sum':sum}
    print(context)
    return render(request, 'DiningServer/shopping.html', context)

# 创建订单 创建完成后自动跳转到支付页面
def createOrder(request):
    """
    创建订单接口
    :param request:
    :return:
    """
    order_service.createOrder()
    return HttpResponse('success')

@require_POST
def payOrder(request):
    """
    用户支付订单接口
    :param request:
    :return:
    """
    order_service.payOrder()
    return HttpResponse('success')

def getOrders(request):
    """
    获取用户订单页面
    :param request:
    :return: 返回”我的订单页面“
    """
    context = order_service.getOrders('abc')
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