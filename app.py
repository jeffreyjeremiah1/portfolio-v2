from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

from config import Config
from models import db, User, Message

from routes.public import public
from routes.admin import admin
from routes.auth import auth

from utils import get_unread_count


# Initialize Flask application

app = Flask(__name__)
app.config.from_object(Config)


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


# Initialize database

db.init_app(app)


# Initialize Flask-Migrate

migrate = Migrate(app, db)



# Register blueprints

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(auth)

# User loader for Flask-Login

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


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
    app.run(debug=True, port=8000)