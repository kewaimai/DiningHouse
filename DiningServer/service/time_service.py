__author__ = '祥祥'

from DiningServer.common.time_format_util import HOUR_AND_MINUTE

import time

"""
获取时间选项
"""
def getTimeOption():
    time_list = []
    minute = time.localtime(time.time())
    stemp_now = time.time()
    print('getTimeOption: print')
    print(minute)
    print('stemp_now: print')
    print(stemp_now)
    local_time = time.strftime(HOUR_AND_MINUTE, time.localtime(stemp_now))
    l_hour , l_minute = [int(i) for i in local_time.split(':')]
    for i in range(15):
        if not l_minute % 15:
            break
        else:
            l_minute += 1
            if l_minute >= 60:
                l_minute = 0
                l_hour += 1
    for i in range(5):
        time_list.append('%02d:%02d' % (l_hour, l_minute))
        # 往后加15分钟
        l_minute += 15
        if l_minute >= 60:
                l_minute = 0
                l_hour += 1

    return time_list