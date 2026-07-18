from flask import Blueprint, render_template, redirect, url_for, flash
from models import db, Project
from forms import ProjectForm


admin = Blueprint("admin", __name__)

@admin.route("/admin")
def dashboard():
    projects = Project.query.all()
    return render_template(
        "admin/dashboard.html",
        projects=projects
    )


@admin.route("/admin/add", methods=["GET", "POST"])
def add_project():

    form = ProjectForm()

    if form.validate_on_submit():

        project = Project(
            title=form.title.data,
            description=form.description.data,
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
def edit_project(id):

    project = Project.query.get_or_404(id)

    form = ProjectForm(obj=project)

    if form.validate_on_submit():

        form.populate_obj(project)

        db.session.commit()

        flash("Project updated successfully!", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/edit_project.html",
        form=form,
        project=project
    )

@admin.route("/admin/delete/<int:id>", methods=["POST"])
def delete_project(id):

    project = Project.query.get_or_404(id)

    db.session.delete(project)
    db.session.commit()

    flash("Project deleted successfully!", "success")

    return redirect(url_for("admin.dashboard"))