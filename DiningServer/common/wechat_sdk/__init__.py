# -*- coding: utf-8 -*-

__all__ = ['WechatBasic', 'WechatExt']

try:
    from DiningServer.common.wechat_sdk.basic import WechatBasic
    from DiningServer.common.wechat_sdk.ext import WechatExt
except ImportError:
    pass