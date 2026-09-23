"""Settings for the salon web app. Everything deployment-specific comes from env vars."""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes", "on")


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-insecure-key-change-me")
DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = [h for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h]
CSRF_TRUSTED_ORIGINS = [o for o in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if o]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "booking",
    "whatsapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "salon_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "booking.context_processors.salon",
                "booking.context_processors.inbox",
            ],
        },
    },
]

WSGI_APPLICATION = "salon_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("SALON_DB_PATH", BASE_DIR / "salon.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("SALON_TIME_ZONE", "Asia/Kolkata")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = Path(os.environ.get("SALON_MEDIA_ROOT", BASE_DIR / "media"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

# --- Salon profile -----------------------------------------------------------
SALON_NAME = os.environ.get("SALON_NAME", "Glow Salon")
SALON_ADDRESS = os.environ.get("SALON_ADDRESS", "")
SALON_CURRENCY = os.environ.get("SALON_CURRENCY", "₹")
# Minutes between bookable start times.
SLOT_INTERVAL_MINUTES = int(os.environ.get("SALON_SLOT_INTERVAL_MINUTES", "30"))
# How many days ahead clients may book over WhatsApp.
BOOKING_WINDOW_DAYS = int(os.environ.get("SALON_BOOKING_WINDOW_DAYS", "14"))
# Send reminders for appointments starting within this many hours.
REMINDER_LEAD_HOURS = int(os.environ.get("SALON_REMINDER_LEAD_HOURS", "24"))

# --- WhatsApp Cloud API (Meta) ----------------------------------------------
# Without WHATSAPP_TOKEN / WHATSAPP_PHONE_NUMBER_ID the app runs in "dry run":
# outbound messages are stored and logged but not sent.
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN", "change-me")
# When set, incoming webhook payloads must carry a valid X-Hub-Signature-256.
WHATSAPP_APP_SECRET = os.environ.get("WHATSAPP_APP_SECRET", "")
WHATSAPP_API_VERSION = os.environ.get("WHATSAPP_API_VERSION", "v21.0")
# Public number clients message, digits only with country code (for wa.me links).
WHATSAPP_PUBLIC_NUMBER = os.environ.get("WHATSAPP_PUBLIC_NUMBER", "")
# Approved template used for reminders, which usually fall outside the 24h
# customer-service window. Params: {{1}} client name, {{2}} service, {{3}} time.
WHATSAPP_REMINDER_TEMPLATE = os.environ.get("WHATSAPP_REMINDER_TEMPLATE", "")
WHATSAPP_TEMPLATE_LANGUAGE = os.environ.get("WHATSAPP_TEMPLATE_LANGUAGE", "en")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "whatsapp": {"handlers": ["console"], "level": "WARNING" if "test" in sys.argv else "INFO"},
    },
}
# Approved template for alerting a stylist about a client chat when they haven't
# messaged the salon number in 24h. Params: {{1}} client name, {{2}} message preview.
WHATSAPP_STAFF_ALERT_TEMPLATE = os.environ.get("WHATSAPP_STAFF_ALERT_TEMPLATE", "")
