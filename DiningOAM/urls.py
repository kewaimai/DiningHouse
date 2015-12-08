__author__ = '祥祥'

from django.conf.urls import url
from . import views

"""
count : 统计 一般表示统计图的数据
"""

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    # 首页
    url(r'^index/$', views.index, name='index'),
    # 用户部分url
    url(r'^getUserNumber/$', views.getUserNumber, name='getUserNumber'),
    url(r'^getUserCount/$', views.getUserCount, name='getUserCount'),
    # 订单部分url
    url(r'^getOrderCount/$', views.getOrderCount, name='getOrderCount'),
    url(r'^getOrderList/$', views.getOrderList, name='getOrderList'),
    # 餐品部分url
    url(r'^getMealList/$', views.getOrderList, name='getMealList'),
    url(r'^updateMealInfo/$', views.updateMealInfo, name='updateMealInfo'),
    url(r'^addMeal/$', views.addMeal, name='addMeal'),
    # 分店部分url
    url(r'^getHouses/$', views.getHouses, name='getHouses'),
    url(r'^addHouse/$', views.addHouse, name='addHouse'),
    url(r'^updateHouseInfo/$', views.updateHouseInfo, name='updateHouseInfo'),
    # 评价部分的url
    url(r'^getAllJudge/$', views.getAllJudge, name='getAllJudge'),
    url(r'^getJudgeDistribute/$', views.getJudgeDistribute, name='getJudgeDistribute'),
]