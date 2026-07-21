from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import form
from models import db, Project, Message
from forms import ProjectForm
import os
from werkzeug.utils import secure_filename
from flask import current_app
from flask_login import login_required


admin = Blueprint("admin", __name__)


@admin.route("/admin")
@login_required
def dashboard():

    total_projects = Project.query.count()

    total_messages = Message.query.count()

    unread_messages = Message.query.filter_by(
        is_read=False
    ).count()

    recent_projects = (
        Project.query
        .order_by(Project.id.desc())
        .limit(5)
        .all()
    )

    recent_messages = (
        Message.query
        .order_by(Message.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin/dashboard.html",
        total_projects=total_projects,
        total_messages=total_messages,
        unread_messages=unread_messages,
        recent_projects=recent_projects,
        recent_messages=recent_messages
    )


@admin.route("/admin/projects")
@login_required
def projects():

    search = request.args.get("search", "").strip()

    page = request.args.get("page", 1, type=int)

    query = Project.query

    if search:
        query = query.filter(
            Project.title.ilike(f"%{search}%")
        )

    projects = (
        query
        .order_by(Project.id.desc())
        .paginate(
            page=page,
            per_page=5,
            error_out=False
        )
    )

    return render_template(
        "admin/projects.html",
        projects=projects,
        search=search
    )


@admin.route("/admin/add", methods=["GET", "POST"])
@login_required
def add_project():

    form = ProjectForm()

    if form.validate_on_submit():
        filename = None

        if form.image.data:

            image = form.image.data

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
    )

        project = Project(
            title=form.title.data,
            description=form.description.data,
            image=f"uploads/{filename}" if filename else None,
            github=form.github.data,
            demo=form.demo.data,
            technologies=form.technologies.data,
        )

        db.session.add(project)
        db.session.commit()

        flash("Project added successfully!", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/add_project.html",
        form=form
    )

@admin.route("/admin/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_project(id):

    project = db.get_or_404(Project, id)

    form = ProjectForm(obj=project)

    if form.validate_on_submit():

        if form.image.data:

            image = form.image.data

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
                )

            project.image = f"uploads/{filename}"

        form.populate_obj(project)

        if filename:
            project.image = f"uploads/{filename}"

        db.session.commit()

        flash("Project updated successfully!", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/edit_project.html",
        form=form,
        project=project
    )

@admin.route("/admin/delete/<int:id>", methods=["POST"])
@login_required
def delete_project(id):

    project = db.get_or_404(Project, id)

    db.session.delete(project)
    db.session.commit()

    flash("Project deleted successfully!", "success")

    return redirect(url_for("admin.dashboard"))


@admin.route("/admin/messages")
@login_required
def messages():

    search = request.args.get("search", "").strip()

    page = request.args.get("page", 1, type=int)

    query = Message.query

    if search:
        query = query.filter(
            (Message.name.ilike(f"%{search}%")) |
            (Message.email.ilike(f"%{search}%")) |
            (Message.subject.ilike(f"%{search}%"))
        )

    messages = (
        query
        .order_by(Message.created_at.desc())
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )

    return render_template(
        "admin/messages.html",
        messages=messages,
        search=search
    )


@admin.route("/admin/messages/<int:id>")
@login_required
def view_message(id):

    message = db.get_or_404(Message, id)

    if not message.is_read:
        message.is_read = True
        db.session.commit()

    return render_template(
        "admin/view_message.html",
        message=message
    )

@admin.route("/admin/messages/delete/<int:id>", methods=["POST"])
@login_required
def delete_message(id):

    message = db.get_or_404(Message, id)

    db.session.delete(message)

    db.session.commit()

    flash(
        "Message deleted successfully.",
        "success"
    )

    return redirect(url_for("admin.messages"))