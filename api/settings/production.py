from .base import *

if not DEBUG:
    ADMINS = [
        ("Muzamil Ali", "mly88207@gmail.com"),
    ]

    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

    # DATABASES = {
    #     "default": dj_database_url.config(
    #         default=env("DATABASE_URL"),
    #         conn_max_age=60,
    #     )
    # }

    # Email setting
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = env("EMAIL_PORT")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    RECIPIENT_ADDRESS = env("RECIPIENT_ADDRESS")
    EMAIL_USE_TLS = True
    SERVER_EMAIL = env("EMAIL_HOST_USER")
