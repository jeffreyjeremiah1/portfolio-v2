from flask import Flask
from config import Config
from models import db

from routes.public import public
from routes.admin import admin



app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(public)
app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(debug=True, port=8000)