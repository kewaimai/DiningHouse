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
    startGenerator()
    return HttpResponse('success hahahaha')

def indextest(request):
    context = meal_service.getCategoryAndList()
    print(context)
    return HttpResponse(str(context))

# 首页page
def index(request):
    #获取用户经纬度，默认使用最近的店面

    context = meal_service.getCategoryAndList()
    return render(request, 'DiningServer/index.html', context)

# 获取商品详情界面
def getMealDetail(request,meal_id):
    # return HttpResponse(json.dumps(meal_service.getMealDetail('1')))
    context = meal_service.getMealDetail(meal_id)
    return render(request, 'DiningServer/details.html', context)

# 获取评价我的订单的界面
def getJudgeMealPage(request):
    return HttpResponse('')

# 评价商品接口
@require_POST
def judgeMeal(request):
    # meal_service.judgeMeal()
    return HttpResponse('')

# 获取商品的评价页面
def getMealJudge(request):
    return HttpResponse('')

# 获取我的订单
def getMyBill(request):
    return render(request, 'DiningServer/myOrder.html', {})

# 获取我的详细信息页面
def getMyDetailInfoPage(request):
    # 获取userid
    # 使用ensure_ascii = False   否则的话中文会只显示编码 不显示汉字
    context = user_service.getMyDetailInfo('abc')
    return render(request, 'DiningServer/userInfoPage.html', context)

# 修改我的详细信息
def modifyMyDetailInfo(request):
    user_service.modifyMyDetailInfo('abc','mingzi','女','1998-10-11','1212312','auisa@qq.com','中关村南大街')
    context = user_service.getMyDetailInfo('abc')
    return render(request, 'DiningServer/userInfoPage.html', context)

"""
去下单 页面
"""
@csrf_exempt
@require_POST
def gotoOrderPage(request):
    #TODO 获取用户id
    user = user_service.getMyDetailInfo('abc')
    meals = meal_service.getMealsAndCount(request.POST)
    times = time_service.getTimeOption()
    context = {'meals':meals, 'user':user, 'times': times}
    print(context)
    return render(request, 'DiningServer/shopping.html', context)

# 创建订单 创建完成后自动跳转到支付页面
def createOrder(request):
    order_service.createOrder()
    return HttpResponse('success')

@require_POST
# 支付订单
def payOrder(request):
    order_service.payOrder()
    return HttpResponse('success')

# 获取用户的订单
def getOrders(request):
    context = order_service.getOrders('abc',1)
    print(context)
    return render(request, 'DiningServer/myOrder.html', context)

def ensureSend(request):
    if order_service.ensureSend('1'):
        return HttpResponse('success')
    else:
        return HttpResponse('error')

def getOrdersByType(request):
    return render(request, 'DiningServer/orders.html')