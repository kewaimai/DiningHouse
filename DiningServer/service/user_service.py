from django.core.exceptions import ObjectDoesNotExist
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
    try:
        user = TblUser.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return {}

    detail_info =  {
        'id' : user.id,
        'username' : user.username,
        'sex' : user.sex,
        'birthday' : user.birthday.strftime(SERVER_DATA_FORMAT),
        'phone' : user.phone,
        'email' : user.email,
        'location' : user.user_location
    }
    return detail_info


# 更改用户详细信息
def modifyMyDetailInfo(user_id, username, sex, birthday, phone, email, add_time, location, latitude, longitude):
    # user = TblUser()
    # user.id = user_id
    # user.username = username
    # user.sex = sex
    # user.birthday = birthday
    # user.phone = phone
    # user.email = email
    # user.add_time = add_time
    # user.location = location
    # user.latitude = latitude
    # user.longitude = longitude
    # user.save()

    TblUser.objects.filter(id=user_id).update(
                                            username=username,
                                            sex=sex,
                                            birthday=birthday,
                                            phone=phone,
                                            email=email,
                                            add_time=add_time,
                                            user_location=location,
                                            latitude=latitude,
                                            longitude=longitude
                                            )