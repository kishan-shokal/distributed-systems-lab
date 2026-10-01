from .base import *

load_dotenv(BASE_DIR / ".env.local",override=True)

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]


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
