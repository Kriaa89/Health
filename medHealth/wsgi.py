"""
WSGI config for medHealth project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medHealth.settings')

application = get_wsgi_application()
