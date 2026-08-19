import os
from dotenv import load_dotenv

load_dotenv()


def _normalize_db_url(url):
    """
    Fall back to local SQLite if no DATABASE_URL is set, and
    rewrite the legacy 'postgres://' scheme (still handed out by
    some hosts) to the 'postgresql://' scheme SQLAlchemy requires.
    """

    if not url:
        return "sqlite:///portfolio.db"

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    return url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Explicit rather than relying on the browser's implicit default.
    SESSION_COOKIE_SAMESITE = "Lax"

    SQLALCHEMY_DATABASE_URI = _normalize_db_url(os.getenv("DATABASE_URL"))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Avoids "server closed the connection unexpectedly" errors on hosts
    # that silently drop idle Postgres connections; a no-op for SQLite.
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }

    UPLOAD_FOLDER = "static/uploads"

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    # File storage backend: "local" (default) writes to static/uploads on
    # disk. Set STORAGE_BACKEND=s3 and the S3_* vars below to instead
    # persist uploads to S3-compatible object storage (needed on hosts
    # with an ephemeral filesystem, since local disk is wiped on redeploy).
    STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")

    S3_BUCKET = os.getenv("S3_BUCKET")
    S3_REGION = os.getenv("S3_REGION")
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")  # for non-AWS S3-compatible providers
    S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
    S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
    S3_PUBLIC_URL = os.getenv("S3_PUBLIC_URL")  # e.g. CDN/base URL to prefix stored keys with

    # Error monitoring: leave unset locally. Set SENTRY_DSN in production
    # to start reporting unhandled exceptions to Sentry.
    SENTRY_DSN = os.getenv("SENTRY_DSN")

    # Set to "1" once the app is deployed behind a host/proxy that
    # terminates TLS and forwards X-Forwarded-Proto correctly. Leave
    # "0" for local dev (plain http) to avoid redirect loops.
    FORCE_HTTPS = os.getenv("FORCE_HTTPS", "0") == "1"

    # Shared storage backend for Flask-Limiter's rate-limit counters.
    # Default is in-memory, which is fine for a single-process dev
    # server but does NOT share state across multiple gunicorn workers.
    # Set to a Redis URL (e.g. redis://localhost:6379) in production
    # if running with more than one worker.
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")

    # Optional email notification when a new contact message arrives
    # (see notifications.py). Leave SMTP_HOST/NOTIFY_EMAIL unset to
    # disable entirely — messages still save to the admin inbox either way.
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_FROM = os.getenv("SMTP_FROM")
    NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL")