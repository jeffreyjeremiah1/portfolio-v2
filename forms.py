from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms import BooleanField
from wtforms import TextAreaField
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