"""
Django settings for lfis_school project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-lfis-school-secret-key-change-in-production-2024'

DEBUG = True

ALLOWED_HOSTS = ['*']

# ─── Jazzmin Admin Theme ────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "LFIS Admin",
    "site_header": "LFIS School Admin",
    "site_brand": "LFIS",
    "site_logo": None,  # Will be overridden by SiteSettings if logo uploaded
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "🎓 Welcome to LFIS School Management Panel",
    "copyright": "Little Flower International School — Admin Panel",
    "search_model": ["auth.user"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Website", "url": "/", "new_window": True},
        {"model": "auth.User"},
    ],
    "usermenu_links": [
        {"name": "View Website", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "core",
        "core.SiteSettings",
        "core.ContactInfo",
        "core.SocialMedia",
        "core.Banner",
        "core.Popup",
        "core.About",
        "gallery",
        "notice_board",
        "academics",
        "facilities",
        "staff",
        "enquiry",
        "tc",
        "alumni",
        "school_messages",
        "corner",
        "captain",
        "house",
        "prospectus",
        "disclosure",
        "auth",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.SiteSettings": "fas fa-cog",
        "core.ContactInfo": "fas fa-phone-alt",
        "core.SocialMedia": "fas fa-share-alt",
        "core.Banner": "fas fa-images",
        "core.Popup": "fas fa-bell",
        "core.About": "fas fa-school",
        "gallery.Album": "fas fa-folder-open",
        "gallery.Photo": "fas fa-camera",
        "gallery.Video": "fas fa-video",
        "notice_board.Notice": "fas fa-bullhorn",
        "academics.FeeStructure": "fas fa-rupee-sign",
        "facilities.Facility": "fas fa-building",
        "staff.Staff": "fas fa-chalkboard-teacher",
        "enquiry.Enquiry": "fas fa-user-plus",
        "tc.TC": "fas fa-file-alt",
        "alumni.Alumni": "fas fa-graduation-cap",
        "school_messages.DirectorMessage": "fas fa-user-tie",
        "school_messages.PrincipalMessage": "fas fa-chalkboard-teacher",
        "captain.SchoolCaptain": "fas fa-star",
        "house.House": "fas fa-flag",
        "prospectus.Prospectus": "fas fa-book",
        "disclosure.Disclosure": "fas fa-landmark",
        "corner.Corner": "fas fa-users",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "css/admin_custom.css",
    "custom_js": "js/admin_color_preview.js",
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-navy",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": False,
}
# ────────────────────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    'jazzmin',  # MUST be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'ckeditor',
    'ckeditor_uploader',
    'import_export',
    'adminsortable2',

    # Local apps
    'core',
    'gallery',
    'notice_board',
    'tc',
    'disclosure',
    'facilities',
    'school_messages',
    'academics',
    'corner',
    'captain',
    'house',
    'prospectus',
    'alumni',
    'staff',
    'enquiry',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lfis_school.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'lfis_school.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lfis_db',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEditor configuration
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'extraPlugins': ','.join([
            'uploadimage',
            'image2',
        ]),
    },
}

# Silence CKEditor 4 security warning
SILENCED_SYSTEM_CHECKS = ['ckeditor.W001']
