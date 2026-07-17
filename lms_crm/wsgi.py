# File: backend/lms_crm/wsgi.py
# WSGI application entrypoint for WSGI servers (Developed by SAYAB)

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_crm.settings")

application = get_wsgi_application()
