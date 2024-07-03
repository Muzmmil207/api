from .base import *

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    # MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")
    # INSTALLED_APPS.append("django_browser_reload")
