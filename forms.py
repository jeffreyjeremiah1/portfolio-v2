from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms import IntegerField
from flask_wtf.file import MultipleFileField
from wtforms.validators import DataRequired
from wtforms import BooleanField
from wtforms import TextAreaField
from wtforms import EmailField
from wtforms.validators import Email, Length, EqualTo


class LoginForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")


class ProjectForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description",
        validators=[DataRequired()]
    )

    github = StringField("GitHub")

    demo = StringField("Demo")

    technologies = StringField("Technologies")

    submit = SubmitField("Save Project")

    image = FileField(
    "Project Image",
        validators=[
            FileAllowed(["jpg", "jpeg", "png", "webp"], "Images only!")
        ]
    )

    gallery = MultipleFileField(
        "Project Gallery",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only."
            )
        ]
    )

    featured = BooleanField("Featured Project")

    published = BooleanField(
        "Published",
        default=True
    )

    display_order = IntegerField(
        "Display Order",
        default=0
    )

    
class ContactForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    subject = StringField(
        "Subject",
        validators=[
            DataRequired()
        ]
    )

    message = TextAreaField(
        "Message",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Send Message"
    )

class EditProfileForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=100)],
        render_kw={"placeholder": "Enter username"}
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter email"}
    )

    profile_image = FileField(
        "Profile Picture",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only!"
            )
        ]
    )

    submit = SubmitField("Save Changes")

class ChangePasswordForm(FlaskForm):

    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired()]
    )

    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "new_password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField("Update Password")


class SettingsForm(FlaskForm):

    # General
    site_name = StringField(
        "Site Name",
        validators=[DataRequired(), Length(max=100)]
    )

    tagline = StringField("Tagline")

    about = TextAreaField("About")

    # Contact
    contact_email = EmailField(
        "Contact Email",
        validators=[
            Email(),
            Length(max=120)
        ]
    )

    phone = StringField("Phone")

    address = StringField("Address")

    # Social
    github = StringField("GitHub")

    linkedin = StringField("LinkedIn")

    twitter = StringField("X (Twitter)")

    facebook = StringField("Facebook")

    instagram = StringField("Instagram")

    youtube = StringField("YouTube")

    # SEO
    meta_title = StringField("Meta Title")

    meta_description = TextAreaField("Meta Description")

    meta_keywords = StringField("Meta Keywords")

    # logo and favicon
    logo = FileField(
    "Site Logo",
    validators=[
        FileAllowed(
            ["jpg", "jpeg", "png", "webp"],
            "Images only."
        )
    ]
    )

    favicon = FileField(
        "Favicon",
        validators=[
            FileAllowed(
                ["png", "ico"],
                "PNG or ICO only."
            )
        ]
    )

    # Footer
    copyright_text = StringField("Copyright")

    submit = SubmitField("Save Settings")