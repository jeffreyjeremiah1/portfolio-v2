from app import app
from models import db, User

with app.app_context():

    if not User.query.filter_by(username="admin").first():

        user = User(username="admin")
        user.set_password("campmulla766")

        db.session.add(user)
        db.session.commit()

        print("Admin user created.")

    else:
        print("Admin user already exists.")