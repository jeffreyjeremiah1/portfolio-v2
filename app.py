import os

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_talisman import Talisman
from flask_wtf import CSRFProtect

from config import Config
from extensions import limiter
from models import db, User, Message, Settings

from routes.public import public
from routes.admin import admin
from routes.auth import auth

from utils import get_unread_count, upload_url


# Error monitoring (opt-in): only activates when SENTRY_DSN is set, so
# local dev needs no Sentry account/config at all.
if os.getenv("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )


# Initialize Flask application

app = Flask(__name__)
app.config.from_object(Config)


# Security headers (HSTS, X-Frame-Options, CSP, etc). CSP is scoped to the
# CDNs already used in templates/base.html (Bootstrap, GLightbox, Quill,
# Google Fonts, Font Awesome). 'unsafe-inline' is required for the small
# inline <script>/style blocks already present (theme flip, GLightbox init)
# — this repo has no build step to hash/nonce them.
csp = {
    "default-src": "'self'",
    "script-src": [
        "'self'",
        "'unsafe-inline'",
        "https://cdn.jsdelivr.net",
    ],
    "style-src": [
        "'self'",
        "'unsafe-inline'",
        "https://cdn.jsdelivr.net",
        "https://cdnjs.cloudflare.com",
        "https://fonts.googleapis.com",
    ],
    "font-src": [
        "'self'",
        "https://fonts.gstatic.com",
        "https://cdnjs.cloudflare.com",
        "data:",
    ],
    "img-src": ["'self'", "data:", "https:"],
    "connect-src": "'self'",
}

Talisman(
    app,
    force_https=app.config["FORCE_HTTPS"],
    strict_transport_security=app.config["FORCE_HTTPS"],
    content_security_policy=csp,
    session_cookie_secure=app.config["FORCE_HTTPS"],
)


# Rate limiting (brute-force / spam protection on login + contact form).
# No blanket default_limits here on purpose — a global per-IP cap would
# also count every CSS/JS/image request through /static and quickly
# lock out real visitors just browsing the site. Instead, only the
# specific routes that need it (login, contact form) carry an explicit
# @limiter.limit(...) decorator in routes/auth.py and routes/public.py.
# See config.py RATELIMIT_STORAGE_URI for the multi-worker caveat.
# The Limiter instance itself lives in extensions.py so route modules
# can import it and decorate specific routes without a circular import
# back to app.py.
limiter.init_app(app)


# Context processor to inject unread messages count into templates
@app.context_processor
def inject_admin_stats():
    if current_user.is_authenticated:
        return {
            "unread_messages": get_unread_count()
        }
    return {"unread_messages": 0}



# Initialize Flask-Login

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"

login_manager.login_message = "Please log in to continue."

login_manager.login_message_category = "warning"


# Initialize CSRF protection for all state-changing routes

csrf = CSRFProtect(app)


# Initialize database

db.init_app(app)


# Initialize Flask-Migrate

migrate = Migrate(app, db)


# Make upload_url() available in all templates for rendering uploaded
# images/files (resolves to local /static or S3 depending on STORAGE_BACKEND)
app.jinja_env.globals["upload_url"] = upload_url


# Register blueprints

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(auth)


# User loader for Flask-Login

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Context processor to inject settings into templates
@app.context_processor
def inject_settings():
    return {
        "settings": Settings.query.first()
    }

# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, port=8000)