"""
WSGI config for DiningHouse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DiningHouse.settings")
#
# application = get_wsgi_application()

import os,sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DiningHouse.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
