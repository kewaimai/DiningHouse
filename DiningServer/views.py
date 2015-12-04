from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from DiningServer.service import meal_service
from DiningServer.service import user_service
import json

from django.views.decorators.http import require_POST
from DiningServer.read_excel import startGenerator

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
    print(context)
    return render(request, 'DiningServer/index.html', context)

# 获取商品详情界面
def getMealDetail(request):
    return HttpResponse(json.dumps(meal_service.getMealDetail('1')))

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
    return HttpResponse('')

# 获取我的详细信息页面
def getMyDetailInfoPage(request):
    # 获取userid
    # 使用ensure_ascii = False   否则的话中文会只显示编码 不显示汉字
    return HttpResponse(json.dumps(user_service.getMyDetailInfo('abc'), ensure_ascii=False))

# 修改我的详细信息
def modifyMyDetailInfo(request):
    user_service.modifyMyDetailInfo('abc','mingzi','女','1998-10-11','1212312','auisa@qq.com','中关村南大街')
    return HttpResponse('success')