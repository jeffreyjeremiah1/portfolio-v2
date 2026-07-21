from flask import Blueprint, render_template
from models import Project
from forms import ContactForm
from models import db, Message, Project
from flask import flash, redirect, url_for


public = Blueprint("public", __name__)


@public.route("/", methods=["GET", "POST"])
def home():

    form = ContactForm()

    projects = Project.query.all()

    if form.validate_on_submit():

        message = Message(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )

        db.session.add(message)
        db.session.commit()

        flash(
            "Message sent successfully!",
            "success"
        )

        return redirect(url_for("public.home"))

    return render_template(
        "home.html",
        projects=projects,
        form=form
    )

