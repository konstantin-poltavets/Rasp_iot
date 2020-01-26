import os
import time
import traceback
import signal
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/pi/iot/myhome')
# adjust the Python version in the line below as needed
sys.path.append('/home/pi/iot/venv/lib/python3.5/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")

try:
    application = get_wsgi_application()
except Exception:
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)


# -*- coding: utf-8 -*-

#import  site
#sys.path.insert(0, os.path.dirname(__file__))
#site.addsitedir('/home/pi/iot/venv/lib/python3.5/site-packages')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'myhome.settings'
#from django.core.handlers.wsgi import WSGIHandler
#application = WSGIHandler()
