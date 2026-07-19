from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config
from models import db, User

from routes.public import public
from routes.admin import admin
from routes.auth import auth


# Initialize Flask application

app = Flask(__name__)
app.config.from_object(Config)


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
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True, port=8000)