"""
WSGI config for GladFood project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""
import sys

sys.path.append('D:\home\site\wwwroot\env\Lib\site-packages')

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GladFood.settings')

application = get_wsgi_application()
