# -*- coding: utf-8 -*-

default_app_config = 'wechat_sdk.context.framework.django.apps.ContextConfig'

try:
    from DiningServer.common.wechat_sdk.context.framework.django.models import Context as DatabaseContext
    from DiningServer.common.wechat_sdk.context.framework.django.backends.db import ContextStore as DatabaseContextStore
except ImportError:
    pass