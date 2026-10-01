from .base import *
import os

load_dotenv(BASE_DIR / ".env.production", override=True)

DEBUG = False

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    ""
).split(",")


DATABASES = {
    "default": {
        "ENGINE": os.getenv(
            "DB_ENGINE",
            "django.db.backends.mysql"
        ),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "3306"),
    }
}


STATIC_ROOT = BASE_DIR / "staticfiles"


SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True