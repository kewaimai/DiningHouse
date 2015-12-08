__author__ = '祥祥'

from DiningServer.models import TblBill
from DiningServer.models import TblBillMeal

from DiningServer.interface import MyBill

from DiningServer.common.time_format_util import SERVER_TIME_FORMAT_WITHOUT_SECOND
from DiningServer.common.time_format_util import SERVER_TIME_FORMAT
from uuid import uuid4
import time

"""
订单相关服务
"""

# 1,未付款    2，配送中    3，待评价
bill_state = [
    '全部',
    '未付款',
    '配送中',
    '待评价'
]
BILL_STATE_ALL = 0
BILL_STATE_UNPAY = 1
BILL_STATE_SENDING = 2
BILL_STATE_JUDGE = 3
BILL_STATE_JUDGED = 4       #这个状态的订单不再显示到用户的订单列表里


def createOrder():
    #TODO 创建订单
    time_now = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
    bill = TblBill()
    bill.id = uuid4()
    # bill.user_id = user_id
    # userlocation——id不再使用  用户表里存入用户的location
    # bill.user_location_id
    # bill.bill_totalling =
    bill.add_time = time_now
    bill.bill_state = BILL_STATE_UNPAY
    bill.bill_content = ''
    bill.save()

    #TODO 保存订单中的商品
    bill_meal = TblBillMeal()
    bill_meal.id = uuid4()
    bill_meal.add_time = time_now
    bill_meal.bill_id = bill.id
    # bill_meal.meal_in_house_id =
    # bill_meal.buy_count =
    bill_meal.save()
    bill_meal.meal_price = 1.0
    pass

"""
如果支付成功 则返回非None 如果失败 返回None
"""
def payOrder(bill_id):
    # 查询订单状态 如果不是等待支付 则返回对应的订单的状态
    bill = TblBill.objects.filter(id=bill_id)
    for item in bill:
        if item.bill_state != BILL_STATE_UNPAY:
            return None

    #TODO 支付订单
    pay_result = False

    # 如果支付成功
    if pay_result:
        for item in bill:
            item.bill_state = BILL_STATE_SENDING
            item.pay_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
            item.save()
    pass

"""
获取用户订单，根据用户输入的用户id和订单类型（未付款，派送中，待评价）返回用户订单列表
"""
def getOrders(user_id, orderType = 0):
    print('=',orderType,'=')
    if orderType != 0:
        print('select by type', orderType)
        myOrder = TblBill.objects.filter(user_id=user_id,bill_state=orderType)
    else:
        print('not by type')
        myOrder = TblBill.objects.filter(user_id=user_id)
    myBill = MyBill()
    for item in myOrder:
        add_time = ''
        pay_time = ''
        ensure_send_time = ''
        if item.add_time:
            add_time = item.add_time.strftime(SERVER_TIME_FORMAT_WITHOUT_SECOND)
        if item.pay_time:
            pay_time = item.pay_time.strftime(SERVER_TIME_FORMAT_WITHOUT_SECOND)
        if item .ensure_send_time:
            ensure_send_time = item.ensure_send_time.strftime(SERVER_TIME_FORMAT_WITHOUT_SECOND)
        myBillIndex = myBill.createBill(
            item.id,
            item.user_id,
            item.user_location,
            item.bill_totalling,
            add_time,
            pay_time,
            bill_state[item.bill_state],
            item.bill_content,
            ensure_send_time
        )
        myMeals = TblBillMeal.objects.filter(bill_id=item.id)
        for meal in myMeals:
            myBill.addMeal(myBillIndex, meal.meal_in_house_id, meal.meal_name, meal.meal_url, meal.buy_count, meal.meal_price)
    return myBill.toDict()

# 确认送达 可有商户或者用户两方调用
def ensureSend(bill_id):
    bill = TblBill.objects.filter(id=bill_id)
    for item in bill:
        # 如果不是正在派送的状态，则返回失败
        if item.bill_state != BILL_STATE_SENDING:
            return None
        # 更改状态为待评价
        item.bill_state = BILL_STATE_JUDGE
        item.ensure_send_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
        item.save()
        break
    else:
        return None
    return 'success'