 __author__ = '祥祥'

from django.conf.urls import url
from . import views


urlpatterns = [
    #for test
    url(r'^indextest/$', views.indextest , name='indextest'),
    url(r'^generatorMeals/$', views.generatorMeals),

    # index  首页 url
    url(r'^index/$', views.index, name='index'),
    # 获取某个分类的餐品内容
    # url(r'^(?P<category_id>[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/getMealsFromCategory/$', views.getMealsFromCategory, )

    # 获取商品的评价界面
    url(r'^getJudgeMealPage/$', views.getJudgeMealPage, name='getJudgeMealPage'),
    # 获取商品评价
    url(r'^getMealJudge/$', views.getMealJudge, name='getMealJudge'),
    # 评价商品
    url(r'^judgeMeal/$', views.judgeMeal, name='judgeMeal'),

    # 获取商品详情页面
    url(r'^(?P<meal_id>[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/getMealDetail/$', views.getMealDetail, name='getMealDetail'),

    # 获取我的订单页面 未付款 配送中 待评价
    url(r'^getMyBill/$', views.getMyBill, name='getMyBill'),

    # 获取我的资料 、更新资料
    url(r'^getMyDetailInfoPage/$', views.getMyDetailInfoPage, name='getMyDetailInfoPage'),
    url(r'^modifyMyDetailInfo/$', views.modifyMyDetailInfo, name='modifyMyDetailInfo'),

    # 我的钱包

    # 下单
    # 去下单页面
    url(r'^gotoOrderPage/$', views.gotoOrderPage, name='gotoOrderPage'),
    # 创建订单接口      返回创建订单成功并提示去支付  的界面
    url(r'^createOrder/$', views.createOrder, name='createOrder'),
    # 支付订单接口
    url(r'^payOrder/$', views.payOrder, name='payOrder'),
    url(r'^getOrders/$', views.getOrders, name='getOrder'),
    url(r'^ensureSend/$', views.ensureSend),
    url(r'^getOrdersByType', views.getOrdersByType, name='ordersByType'),

    # 测试修改
    # 支付接口

    #测试啦啦啦
]