from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

"""
这里是外卖餐厅OAM后台
"""

def login(request):
    return HttpResponse('login')

def index(request):
    return HttpResponse('index')


"""
用户接口部分
"""

def getUserNumber(request):
    """
    获取用户数量
    :param request: http request
    :return: 显示用户数量的json
    """
    return HttpResponse('')

def getUserCount(request):
    """
    获取用户统计数量
    :param request:
    :return: 每日用户关注数量
    """
    return HttpResponse('')

"""
订单接口部分
"""

def getOrderCount(request):
    """
    获取订单统计
    :param request: http request
    :return: 用户订单统计的json结果
    """
    return HttpResponse('')

def getOrderList(request):
    """
    获取订单列表
    :param request:
    :return:
    """
    return HttpResponse('')

"""
餐品接口部分
"""

def getMealList(request):
    """
    获取已经录入的餐品列表
    :param request:
    :return:
    """
    return HttpResponse('')

def updateMealInfo(request):
    """
    更新餐品信息 包括餐品的显示顺序
    :param request:
    :return:
    """
    return HttpResponse('')

def addMeal(request):
    """
    新增餐品
    :param request:
    :return:
    """
    return HttpResponse('')



"""
商铺（分店位置）接口部分
"""

def getHouses(request):
    """
    获取所有已经录入的分店位置
    :param request:
    :return:
    """
    return HttpResponse('')

def addHouse(request):
    """
    添加分店
    :param request:
    :return:
    """
    return HttpResponse('')

def updateHouseInfo(request):
    """
    更新分店信息
    :param request:
    :return:
    """
    return HttpResponse('')


"""
获取评分 相关接口
"""
def getAllJudge(request):
    """
    获取全部评分
    :param request:
    :return:
    """
    return HttpResponse('')

def getJudgeDistribute():
    """
    获取评分的分布
    :return:
    """
    return HttpResponse('')