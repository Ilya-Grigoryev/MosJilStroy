# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1370009/data/www/mosjilstroy.ru/MosJilStroy')
sys.path.insert(1, '/var/www/u1370009/data/venv/lib/python3.8.8/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'MosJilStroy.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
