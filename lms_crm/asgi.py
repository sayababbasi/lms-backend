# File: backend/lms_crm/asgi.py
# ASGI application entrypoint for async servers (Developed by SAYAB)

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_crm.settings")

application = get_asgi_application()
