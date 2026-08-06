from flask import Blueprint, render_template
from models import Project
from forms import ContactForm
from models import db, Message, Project
from flask import flash, redirect, url_for


public = Blueprint("public", __name__)


@public.route("/", methods=["GET", "POST"])
def home():

    form = ContactForm()

    projects = (
        Project.query
        .filter_by(
            published=True,
            featured=True
        )
        .order_by(Project.display_order.asc())
        .all()
    )

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

@public.route("/projects/<slug>")
def project_detail(slug):

    project = Project.query.filter_by(
        slug=slug,
        published=True
    ).first_or_404()

    previous_project = (
        Project.query
        .filter(
            Project.id < project.id,
            Project.published == True
        )
        .order_by(Project.id.desc())
        .first()
    )

    next_project = (
        Project.query
        .filter(
            Project.id > project.id,
            Project.published == True
        )
        .order_by(Project.id.asc())
        .first()
    )

    related_projects = (
        Project.query
        .filter(
            Project.id != project.id,
            Project.published == True
        )
        .limit(3)
        .all()
    )

    return render_template(
        "project_detail.html",
        project=project,
        previous_project=previous_project,
        next_project=next_project,
        related_projects=related_projects
    )