from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField, TextAreaField, EmailField, DateField, SelectMultipleField
from wtforms.validators import Email, Length, EqualTo, Optional, DataRequired, Regexp, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput


def validate_pdf_content(form, field):
    """
    FileAllowed only checks the extension, so a renamed non-PDF file
    would otherwise pass. Reject anything whose content doesn't start
    with the PDF magic bytes.
    """

    if not field.data or not getattr(field.data, "filename", None):
        return

    header = field.data.stream.read(5)
    field.data.stream.seek(0)

    if header != b"%PDF-":
        raise ValidationError("File does not look like a valid PDF.")


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

    github = StringField(
        "GitHub",
        validators=[
            Optional(),
            Regexp(r"(?i)^https?://", message="Must be a valid http(s) URL.")
        ]
    )

    demo = StringField(
        "Demo",
        validators=[
            Optional(),
            Regexp(r"(?i)^https?://", message="Must be a valid http(s) URL.")
        ]
    )

    technologies = StringField("Technologies")

    client = StringField(
        "Client",
        validators=[Optional()]
    )

    role = StringField(
        "Role",
        validators=[Optional()]
    )

    project_date = DateField(
        "Project Date",
        validators=[Optional()]
    )

    duration = StringField(
        "Duration",
        validators=[Optional()]
    )

    challenge_text = TextAreaField(
        "The Challenge",
        validators=[Optional()]
    )

    solution_text = TextAreaField(
        "The Solution",
        validators=[Optional()]
    )

    development_process = TextAreaField(
        "Development Process",
        validators=[Optional()]
    )

    results_text = TextAreaField(
        "Results / Outcome",
        validators=[Optional()]
    )

    lessons_text = TextAreaField(
        "Lessons Learned",
        validators=[Optional()]
    )

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

    tags = SelectMultipleField(
        "Tags",
        coerce=int,
        validators=[Optional()],
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput()
    )


class TagForm(FlaskForm):

    name = StringField(
        "Tag Name",
        validators=[DataRequired(), Length(max=50)]
    )

    submit = SubmitField("Save Tag")


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

    # Honeypot spam trap: real visitors never see or fill this field
    # (hidden off-screen via CSS in components/contact.html). Bots that
    # blindly fill every input tend to fill it, so a non-empty value
    # means "reject silently" in the route handler.
    website = StringField(
        "Website",
        validators=[Optional()]
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
        ],
        render_kw={"minlength": "8"}
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

    resume = FileField(
        "Resume (PDF)",
        validators=[
            FileAllowed(
                ["pdf"],
                "PDF only."
            ),
            validate_pdf_content
        ]
    )

    # Footer
    copyright_text = StringField("Copyright")

    submit = SubmitField("Save Settings")


class TestimonialForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[DataRequired(), Length(max=100)]
    )

    role_company = StringField(
        "Role / Company",
        validators=[Optional(), Length(max=150)]
    )

    quote = TextAreaField(
        "Quote",
        validators=[DataRequired()]
    )

    avatar = FileField(
        "Avatar",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only."
            )
        ]
    )

    published = BooleanField(
        "Published",
        default=True
    )

    display_order = IntegerField(
        "Display Order",
        default=0
    )

    submit = SubmitField("Save Testimonial")


class PostForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=150)]
    )

    excerpt = StringField(
        "Excerpt",
        validators=[Optional(), Length(max=300)]
    )

    content = TextAreaField(
        "Content",
        validators=[DataRequired()]
    )

    cover_image = FileField(
        "Cover Image",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only."
            )
        ]
    )

    published = BooleanField(
        "Published",
        default=True
    )

    submit = SubmitField("Save Post")