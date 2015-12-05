__author__ = '祥祥'

from DiningServer.common.time_format_util import HOUR_AND_MINUTE

import time

"""
获取时间选项 返回 “立即送达”
"""
def getTimeOption():
    time_list = ['立即送出']
    minute = time.localtime(time.time())
    stemp_now = time.time()
    time_list.extend([time.strftime(HOUR_AND_MINUTE, time.localtime(stemp_now + i * 900)) for i in range(2,6)])
    return time_list