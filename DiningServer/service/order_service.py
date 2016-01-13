from django.core.exceptions import ObjectDoesNotExist

from DiningServer.models import TblBill
from DiningServer.models import TblBillMeal
from DiningServer.models import TblUser
from DiningServer.interface import MyBill
from DiningServer.service import meal_service

from DiningServer.common.time_format_util import SERVER_TIME_FORMAT_WITHOUT_SECOND
from DiningServer.common.time_format_util import SERVER_TIME_FORMAT
from DiningServer.common.func import *

from uuid import uuid4
import time


"""
订单相关服务
"""

# 1,未付款    2，配送中    3，待评价
# bill_state = [
#     '全部',
#     '未付款',
#     '配送中',
#     '待评价',
#     '已评价'
# ]
# BILL_STATE_ALL = 0
# BILL_STATE_UNPAY = 1
# BILL_STATE_SENDING = 2
# BILL_STATE_JUDGE = 3
# BILL_STATE_JUDGED = 4       #这个状态的订单不再显示到用户的订单列表里

(BILL_STATE_ALL,BILL_STATE_UNPAY,BILL_STATE_SENDING,BILL_STATE_JUDGE,BILL_STATE_JUDGED)=range(5)
bill_state = [
            (BILL_STATE_ALL,'全部'),
            (BILL_STATE_UNPAY,'未付款'),
            (BILL_STATE_SENDING,'配送中'),
            (BILL_STATE_JUDGE,'待评价'),
            (BILL_STATE_JUDGED,'已评价'),
            ]


def createOrder(request):
    # 更改用户信息
    user_id = request.COOKIES.get('user_id')
    username = request.POST.get('username','').strip()
    phone    = request.POST.get('phone','').strip()
    location = request.POST.get('location','').strip()
    user = TblUser.objects.filter(id=user_id).update(username=username,phone=phone,user_location=location)

    time_now = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
    meals = meal_service.getMealsAndCount(request.POST)
    # count = 0
    sum = 0

    buy_meals = meals['meal_list']

    # 获取sum和count
    for meal in buy_meals:
        # count += int(meal['buy_count'])
        sum += int(meal['buy_count']) * float(meal['meal_price'])

    # 创建订单
    bill = TblBill()
    bill.id = uuid4()
    bill.house_id = request.COOKIES.get('house_id','e55ce56e-fcc3-4d55-8da8-73720e569652')
    bill.user_id = request.COOKIES.get('user_id','abc')
    bill.user_location = location
    bill.bill_totalling = sum
    bill.add_time = time_now
    bill.bill_state = BILL_STATE_UNPAY
    bill.bill_content = request.POST.get('remarks','')
    print('request.POST:',request.POST)
    bill.save()
    
    return bill

"""
如果支付成功 则返回非None 如果失败 返回None
"""
def payOrder(request,bill_id,pay_result):
    import logging
    logger = logging.getLogger('django')
    # 查询订单状态 如果不是等待支付 则返回对应的订单的状态
    bill = TblBill.objects.get(id=bill_id)
    if bill.bill_state != BILL_STATE_UNPAY:
        return None

    # 如果支付成功
    if pay_result:
        bill.bill_state = BILL_STATE_SENDING
        bill.pay_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
        bill.save()
    else: return None

"""
获取用户订单，根据用户输入的用户id和订单状态（未付款，派送中，待评价）返回用户订单列表
"""
def getOrders(user_id, orderType = 0):

    myOrder = TblBill.objects.filter(user_id=user_id,bill_state=orderType)
    return myOrder

    # myBill = MyBill()
    # for item in myOrder:
    #     if item.add_time:
    #         add_time = item.add_time.strftime(SERVER_TIME_FORMAT_WITHOUT_SECOND)
    #     if item.pay_time:
    #         pay_time = item.pay_time.strftime(SERVER_TIME_FORMAT_WITHOUT_SECOND)
    #     if item .ensure_send_time:
    #         ensure_send_time = item.ensure_send_time.strftime(SERVER_TIME_FORMAT_WITHOUT_SECOND)
    #     myBillIndex = myBill.createBill(
    #         item.id,
    #         item.user_id,
    #         item.user_location,
    #         item.bill_totalling,
    #         add_time,
    #         pay_time,
    #         bill_state[item.bill_state],
    #         item.bill_content,
    #         ensure_send_time
    #     )
    #     myMeals = TblBillMeal.objects.filter(bill_id=item.id)
    #     for meal in myMeals:
    #         myBill.addMeal(myBillIndex, meal.house_id, meal.meal_name, meal.meal_url, meal.buy_count, meal.meal_price)
    # return myBill.toDict()
    
    
# 确认送达 可有商户或者用户两方调用
def ensureSend(bill_id):
    import logging
    logger = logging.getLogger('django')

    # 如果不是正在派送的状态，则返回失败
    if bill.bill_state != BILL_STATE_SENDING:
        return False

    try:
        bill = TblBill.objects.get(id=bill_id)
    except ObjectDoesNotExist:
        return False
    else:
        # 更改状态为待评价
        bill.bill_state = BILL_STATE_JUDGE
        bill.ensure_send_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
        bill.save()
        return True
    return None