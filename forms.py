from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired


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