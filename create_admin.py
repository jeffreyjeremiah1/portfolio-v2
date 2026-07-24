import getpass
import re

from app import app
from models import db, User


with app.app_context():

    print("\n========== Create Admin Account ==========\n")

    username = input("Username: ").strip()

    if not username:
        print("❌ Username cannot be empty.")
        exit()

    if User.query.filter_by(username=username).first():
        print("❌ Username already exists.")
        exit()

    email = input("Email: ").strip()

    if not email:
        print("❌ Email cannot be empty.")
        exit()

    if User.query.filter_by(email=email).first():
        print("❌ Email already exists.")
        exit()

    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        print("❌ Invalid email address.")
        exit()

    while True:

        password = getpass.getpass("Password: ")
        confirm = getpass.getpass("Confirm Password: ")

        if password != confirm:
            print("❌ Passwords do not match.\n")
            continue

        if len(password) < 8:
            print("❌ Password must contain at least 8 characters.\n")
            continue

        if not re.search(r"[A-Z]", password):
            print("❌ Password must contain an uppercase letter.\n")
            continue

        if not re.search(r"[a-z]", password):
            print("❌ Password must contain a lowercase letter.\n")
            continue

        if not re.search(r"\d", password):
            print("❌ Password must contain a number.\n")
            continue

        break

    user = User(
        username=username,
        email=email
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    print("\n✅ Admin account created successfully!")

    