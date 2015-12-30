__author__ = '祥祥'

from DiningServer.models import TblMealCategory
from DiningServer.models import TblMealInHouse
from DiningServer.models import TblBanner
from DiningServer.models import TblJudgeMeal

from DiningServer.cache import server_cache

from DiningServer import interface
from DiningServer.common.time_format_util import SERVER_TIME_FORMAT
from uuid import uuid4
import time
"""
该服务用于获取跟餐品相关的内容
餐品分类、某分店的商品列表、商品详情等
"""

_in_use_ = 1


def getCategoryAndList():
    import logging
    logger = logging.getLogger('django')
    # 需要返回的数据  商店 banner 分类 第一个分类的餐品
    category_and_meal = interface.CategoryAndMeal()
    #获取菜品分类列表
    #使用缓存
    category_list = []
    # 如果分类数据存在于缓存中 则读缓存
    if server_cache.cache_meal_category:
        print('start get from cache')
        for item in server_cache.cache_meal_category:
            category_list.append(item.id)
            category_and_meal.add_category_and_meals(item.name,item.id)
    # 从数据库中读取 分类数据并存入缓存数据
    else:
        result_list = TblMealCategory.objects.all().order_by('show_order')
        print('len(result_list):',len(result_list))
        for item in result_list:
            print('item:',item)
            category_list.append(item.id)
            category_and_meal.add_category_and_meals(item.name,item.id)
            #add to cache
            print('server_cache.cache_meal_category:',type(server_cache.cache_meal_category))
            server_cache.cache_meal_category.append(item)

    #判断获取的结果
    if not category_list:
        return '{}'

    #banner
    #从缓存中读取banner数据
    if server_cache.cache_banner:
        for item in server_cache.cache_banner:
            category_and_meal.add_banner(item.banner_url, item.link_url)
    else:
        result_list = TblBanner.objects.filter(in_use=_in_use_).order_by('show_order')
        for item in result_list:
            category_and_meal.add_banner(item.banner_url, item.link_url)
            # add to cache
            server_cache.cache_banner.append(item)

    #判断得出需要获取的分店
    category_and_meal.set_house(name='三里屯店',location='三里屯soho地下美食广场', phone='1990009002')

    # 获取分店全部菜品
    house_id = 1    #测试使用的house id
    # 获取第一个分类的商品内容
    meal_list = TblMealInHouse.objects.filter(house_id=house_id).order_by('category_id')
    for item in meal_list:
        index = 0
        if item.category_id in category_list:
            index = category_list.index(item.category_id)
        category_and_meal.add_meals(
            item.id,
            item.name,
            item.avatar_url,
            item.detail_content,
            item.sold_count,
            item.judge_count,
            item.meal_price,
            item.last_count,
            index)
        
    return category_and_meal.to_dict()

"""
获取商品详情
"""
def getMealDetail(id):
    import logging
    logger = logging.getLogger('django')
    tbl_meal_in_house = TblMealInHouse.objects.filter(id=id)

    if len(tbl_meal_in_house) == 1:
        for item in tbl_meal_in_house:
            return interface.getMealDetailDict(
                item.id,
                item.name,
                item.avatar_url,
                item.detail_url,
                item.detail_content,
                item.meal_price,
                item.judge_count,
                item.sold_count,
            )
    else:
        # 如果不唯一就报警了。。。
        pass
    return {}


"""
评价商品
"""
def judgeMeal(bill_id, meal_in_house_id, user_id, user_name, judge_meal, judge_speed, judge_service):
    import logging
    logger = logging.getLogger('django')
    judge_item = TblJudgeMeal()
    judge_item.id = uuid4()
    judge_item.add_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
    judge_item.bill_id = bill_id
    judge_item.meal_in_house = meal_in_house_id
    judge_item.user_id = user_id
    judge_item.user_name = user_name
    judge_item.judge_meal = judge_meal
    judge_item.judge_speed = judge_speed
    judge_item.judge_service = judge_service
    try:
        judge_item.save()
    except Exception as exception:
        print('judge insert error , detail : ', exception)
        return None   # 失败 返回None
    return 'success'   # 成功 返回非None字符串

"""
添加分类
"""
def addCategory(category_name):
    import logging
    logger = logging.getLogger('django')
    count = TblMealCategory.objects.count()
    item = TblMealCategory()
    item.name = category_name
    item.change_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
    item.id = uuid4()
    item.show_order = count + 1  # 显示顺序默认往后排
    item.save()
    return item

def addMealByScript(category_id, category_order, name):
    import logging
    logger = logging.getLogger('django')
    item = TblMealInHouse()
    item.id = uuid4()
    item.add_time = time.strftime(SERVER_TIME_FORMAT, time.localtime(time.time()))
    item.avatar_url = 'http://p1.meituan.net/460.280/deal/__2722145__9710843.jpg'
    item.category_id = category_id
    item.category_order = category_order
    item.detail_content = '米饭：100克DDD菜：100克'
    item.detail_url = 'http://p1.meituan.net/460.280/deal/__2722145__9710843.jpg'
    item.house_id = '1'
    item.judge_count = 2
    item.last_count = 100
    # item.meal_id =
    item.meal_price = 10.0
    item.name = name
    item.sold_count = 120
    item.save()
    pass

"""
获取用户选的商品id的详情 并返回用户选择的数量
"""
def getMealsAndCount(post):
    import logging
    logger = logging.getLogger('django')
    meals_and_count = interface.MealsAndCount()
    print(post)
    for key in post:
        print(key)
        print(post[key])
        tblMeal = TblMealInHouse.objects.filter(id=key)
        for item in tblMeal:
            meals_and_count.add_meals(
                item.id
                , item.name
                , item.avatar_url
                , item.detail_content
                , item.sold_count
                , item.judge_count
                , item.meal_price
                , item.last_count
                , post[key]
            )
            break
    return meals_and_count.toDict()