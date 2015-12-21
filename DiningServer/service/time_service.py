__author__ = '祥祥'

from DiningServer.common.time_format_util import HOUR_AND_MINUTE

import time

"""
获取时间选项
"""
def getTimeOption():
    time_list = []
    local_time = time.strftime(HOUR_AND_MINUTE, time.localtime(time.time()))
    l_hour , l_minute = [int(i) for i in local_time.split(':')]
    
    #按照刻钟获取第一个时间选项
    for i in range(15):
        if not l_minute % 15:
            break
        else:
            l_minute += 1
            if l_minute >= 60:
                l_minute = 0
                l_hour += 1
    #以刻钟为间隔获取五组时间选项
    for i in range(5):
        time_list.append('%02d:%02d' % (l_hour, l_minute))
        l_minute += 15
        if l_minute >= 60:
                l_minute = 0
                l_hour += 1

    return time_list