from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text, nullable=False)

    image = db.Column(db.String(255))

    github = db.Column(db.String(255))

    demo = db.Column(db.String(255))

    technologies = db.Column(db.String(255))

    featured = db.Column(
    db.Boolean,
    default=False
    )

    published = db.Column(
        db.Boolean,
        default=True
    )

    display_order = db.Column(
        db.Integer,
        default=0
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    images = db.relationship(
        "ProjectImage",
        backref="project",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="ProjectImage.display_order"
    )

    client = db.Column(db.String(100))
    role = db.Column(db.String(100))
    project_date = db.Column(db.Date)
    duration = db.Column(db.String(50))

    slug = db.Column(
        db.String(200),
        unique=True,
        nullable=False
    )

    def __repr__(self):
        return f"<Project {self.title}>"
    


class ProjectImage(db.Model):
    __tablename__ = "project_images"

    id = db.Column(db.Integer, primary_key=True)

    image = db.Column(
        db.String(255),
        nullable=False
    )

    caption = db.Column(
        db.String(255)
    )

    display_order = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False
    )



class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    profile_image = db.Column(
        db.String(255),
        default="uploads/profiles/default.png"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    last_login = db.Column(
        db.DateTime,
        nullable=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        nullable=False,
        index=True
    )

    subject = db.Column(
        db.String(200),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    def __repr__(self):
        return f"<Message {self.name}>"



class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)

    # General
    site_name = db.Column(
        db.String(100),
        nullable=False,
        default="My Portfolio"
    )

    tagline = db.Column(db.String(255))

    about = db.Column(db.Text)

    # Contact
    contact_email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(255))

    # Branding
    logo = db.Column(
        db.String(255),
        default="uploads/site/default-logo.png"
    )

    favicon = db.Column(
        db.String(255),
        default="uploads/site/default-favicon.png"
    )

    # Social
    github = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    facebook = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
    youtube = db.Column(db.String(255))

    # SEO
    meta_title = db.Column(db.String(255))
    meta_description = db.Column(db.Text)
    meta_keywords = db.Column(db.String(255))

    # Footer
    copyright_text = db.Column(
        db.String(255),
        default="© 2026 All Rights Reserved."
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )