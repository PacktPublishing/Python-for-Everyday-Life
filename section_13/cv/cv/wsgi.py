# -*- coding: utf-8 -*-
# !/usr/bin/env python3

"""
WSGI config for cv project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cv.settings")

application = get_wsgi_application()
