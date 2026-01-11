# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'billing',
    'django_bootstrap5',
]

# Media / static
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# For production set allowed hosts and configure static/media serving via web server