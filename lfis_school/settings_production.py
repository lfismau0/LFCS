"""
Production settings for PythonAnywhere deployment.
"""

from .settings import *
import os

# Security settings
DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Update this with your PythonAnywhere username
ALLOWED_HOSTS = [
    'lfismau0.pythonanywhere.com',
    'www.lfismau0.pythonanywhere.com',
]

# Database - PythonAnywhere MySQL
# Update these values from your PythonAnywhere MySQL dashboard
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'lfismau0$lfis_db'),
        'USER': os.environ.get('DB_USER', 'lfismau0'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'lfismau0.mysql.pythonanywhere-services.com'),
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

# HTTPS settings (enable once you have SSL)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
