__author__ = '祥祥'

from DiningServer.models import TblUser

from DiningServer.common.time_format_util import SERVER_DATA_FORMAT
import time

SEX = {
    # 从数据库得到数值 从下面得到对应的性别
    1 : '男',
    2 : '女',

    # web端传过来 男女，从下面获取对应的数值
    '男' : 1,
    '女' : 2,
}

# 获取用户详细信息
def getMyDetailInfo(user_id):
    user = TblUser.objects.filter(id=user_id)
    for item in user:
        detail_info =  {
            'id' : item.id,
            'username' : item.username,
            'sex' : item.sex,      # html显示的是选项 所以使用int值判断
            'birthday' : item.birthday.strftime(SERVER_DATA_FORMAT),
            'phone' : item.phone,
            'email' : item.email,
            'location' : item.user_location
        }
        return detail_info
    return {}

# 更改用户详细信息
def modifyMyDetailInfo(user_id, user_name, sex, birthday, phone, email, location):
    user = TblUser()
    user.id = user_id
    user.username = user_name
    user.sex = SEX.get(sex, 0)
    user.birthday = birthday       # 存入数据库的时间 使用string即可
    user.phone = phone
    user.email = email
    user.user_location = location
    user.save()