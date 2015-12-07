__author__ = '祥祥'

"""
页面中获取到的数据
"""



# 首页显示的菜品及内容接口
class CategoryAndMeal():
    """
    最后的context的效果示例
    context = {
        # banners
        'banners':[
            {
                image_url: '这里是图片路径',
                link: '点击后跳转的url'
            },
            {
                image_url: '这里是图片路径',
                link: '点击后跳转的url'
            }
        ]
        # 分店内容  字典表示
        house : {
            'name': '分店名字',
            'location': '分店位置'
        }
        # 分类及菜品 数组
        categorys: [
            # 每一项的分类 字典表示
            {
                'category': '分类1',    # 分类名称
                'category_id': 1,       # 分类id
            },
            {
                'category': '分类2',    # 分类名称
                'category_id': 2,       # 分类id
            },
            {
                'category': '分类3',    # 分类名称
                'category_id': 3,       # 分类id
            },

        ]
        #分类中的菜品 数组表示
        'meals': [
            #菜品中的对象 字典表示
            {
                'meals_id': 1,      # meal id
                'meals_name': '我是菜名',    # 名称
                'avatar_url': '我是图片地址',    # avatar_ur 显示的小图
                'content': '我是描述使用 ddd 分隔每一行的内容',
                'sold_count': 10,            #售出量
                'judge_count': 10,           #评价量
                'meal_price':  10.0,         #单价 元
                'last_count': 20,            #剩余量  0 表示卖完了
            },
            {
                'meals_id': 1,      # meal id
                'meals_name': '我是菜名',    # 名称
                'avatar_url': '我是图片地址',    # avatar_ur 显示的小图
                'content': '我是描述使用 ddd 分隔每一行的内容',
                'sold_count': 10,            #售出量
                'judge_count': 10,           #评价量
                'meal_price':  10.0,         #单价 元
                'last_count': 20,            #剩余量  0 表示卖完了
            }
        ]
    }

    """


    def __init__(self):
        self._context = {}
        self._house = {}
        self._category_and_meal = []
        self._banners = []
        self._meals = [[]]
        self._context['house'] = self._house
        self._context['banners'] = self._banners
        self._context['categorys'] = self._category_and_meal
        self._context['meals'] = self._meals

    def set_house(self, name='', location='', phone=''):
        self._house['name'] = name
        self._house['location'] = location
        self._house['phone'] = phone

    def add_banner(self, image_url='', link=''):
        self._banners.append({
            'image_url':image_url,
            'link': link
        })

    def add_category_and_meals(self, category='', category_id=''):
        self._category_and_meal.append({
            'category': category,
            'category_id': category_id
        })
        self._meals.extend([[]])

    def add_meals(self, meals_id, meals_name, avatar_url, content, sold_count, judge_count, meal_price, last_count, index):
        self._meals[index].append({
            'meals_id': meals_id,
            'meals_name': meals_name,
            'avatar_url': avatar_url,
            'content': content,
            'sold_count': sold_count,
            'judge_count': judge_count,
            'meal_price': meal_price,
            'last_count': last_count,
        })


    def to_dict(self):
        print('餐品的数量', len(self._meals))
        return self._context

# 根据内容构造 商品详情的字典
def getMealDetailDict(id, name, avatar_url, detail_url, detail_content, meal_price, judge_count, sold_count):
    return {
        'id': id,
        'name': name,
        'avatar_url': avatar_url,
        'detail_url': detail_url,
        'detail_content': detail_content.split('DDD'),
        'meal_price': meal_price,
        'judge_count': judge_count,
        'sold_count': sold_count
        }

# 用于构造我的订单页面的返回值
class MyBill():

    def __init__(self):
        self._context = {}
        # bills 是一个账单列表  每个账单包含账单的信息 同时包含一个餐品列表
        self._bills = []
        self._context['bills'] = self._bills

    def createBill(self, id, user_id, user_location, bill_totalling, add_time, pay_time, bill_state, bill_content, ensure_send_time):
        bill = {
            'id': id,
            'user_id': user_id,
            'user_location': user_location,
            'bill_totalling': bill_totalling,
            'add_time': add_time,
            'pay_time': pay_time,
            'bill_state': bill_state,
            'bill_content': bill_content,
            'ensure_send_time': ensure_send_time,
            'meals': []
        }
        self._bills.append(bill)
        return len(self._bills) - 1

    def addMeal(self, bill_order, meal_id, meal_name, meal_url, meal_count, meal_price):
        meal = {
            'meal_id' : meal_id,
            'meal_name' : meal_name,
            'meal_url' : meal_url,
            'meal_count' : meal_count,
            'meal_price' : meal_price
        }
        try:
            self._bills[bill_order]['meals'].append(meal)
        except:
            return None
        return 'success'

    def toDict(self):
        return self._context

"""
餐品和它对应的数量
"""
class MealsAndCount():
    def __init__(self):
        self._context = {}
        self._meal_list = []
        self._context['meal_list'] = self._meal_list

    def add_meals(self, meals_id, meals_name, avatar_url, content, sold_count, judge_count, meal_price, last_count, buy_count):
        self._meal_list.append({
            'meals_id': meals_id,
            'meals_name': meals_name,
            'avatar_url': avatar_url,
            'content': content,
            'sold_count': sold_count,
            'judge_count': judge_count,
            'meal_price': meal_price,
            'last_count': last_count,
            'buy_count' : buy_count,
        })

    def toDict(self):
        return self._context