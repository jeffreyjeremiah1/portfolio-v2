from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import form
from models import db, Project, Message, User, Settings
from forms import ProjectForm, EditProfileForm, ChangePasswordForm, SettingsForm
import os
from werkzeug.utils import secure_filename
from flask import current_app
from flask_login import login_required, current_user
from utils import delete_image, save_image, delete_image
from werkzeug.datastructures import FileStorage


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


@admin.route("/profile")
@login_required
def profile():
    return render_template(
        "admin/profile.html",
        user=current_user
    )

@admin.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():

        username = form.username.data.strip()
        email = form.email.data.strip().lower()

        existing_user = User.query.filter(
            User.username == username,
            User.id != current_user.id
        ).first()

        if existing_user:
            flash("Username already exists.", "danger")
            return render_template("admin/edit_profile.html", form=form)

        existing_email = User.query.filter(
            User.email == email,
            User.id != current_user.id
        ).first()

        if existing_email:
            flash("Email already exists.", "danger")
            return render_template("admin/edit_profile.html", form=form)

        current_user.username = username
        current_user.email = email

        if form.profile_image.data:

            delete_image(current_user.profile_image)

            current_user.profile_image = save_image(
                form.profile_image.data,
                "uploads/profiles",
                (300, 300)
            )

        db.session.commit()

        flash("Profile updated successfully!", "success")
        return redirect(url_for("admin.profile"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template(
        "admin/edit_profile.html",
        form=form
    )


@admin.route("/profile/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    form = ChangePasswordForm()

    if form.validate_on_submit():

        if not current_user.check_password(
            form.current_password.data
        ):

            flash(
                "Current password is incorrect.",
                "danger"
            )

            return render_template(
                "admin/change_password.html",
                form=form
            )

        current_user.set_password(
            form.new_password.data
        )

        db.session.commit()

        flash(
            "Password updated successfully.",
            "success"
        )

        return redirect(
            url_for("admin.profile")
        )

    return render_template(
        "admin/change_password.html",
        form=form
    )


@admin.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    settings = Settings.query.first()


    if settings is None:
        settings = Settings()
        db.session.add(settings)
        db.session.commit()

    form = SettingsForm()



    if request.method == "GET":
        form.site_name.data = settings.site_name
        form.tagline.data = settings.tagline
        form.about.data = settings.about

        form.contact_email.data = settings.contact_email
        form.phone.data = settings.phone
        form.address.data = settings.address

        form.github.data = settings.github
        form.linkedin.data = settings.linkedin
        form.twitter.data = settings.twitter
        form.facebook.data = settings.facebook
        form.instagram.data = settings.instagram
        form.youtube.data = settings.youtube

        form.meta_title.data = settings.meta_title
        form.meta_description.data = settings.meta_description
        form.meta_keywords.data = settings.meta_keywords

        form.copyright_text.data = settings.copyright_text



    if form.validate_on_submit():

        # Update normal text fields
        settings.site_name = form.site_name.data
        settings.tagline = form.tagline.data
        settings.about = form.about.data

        settings.contact_email = form.contact_email.data
        settings.phone = form.phone.data
        settings.address = form.address.data

        settings.github = form.github.data
        settings.linkedin = form.linkedin.data
        settings.twitter = form.twitter.data
        settings.facebook = form.facebook.data
        settings.instagram = form.instagram.data
        settings.youtube = form.youtube.data

        settings.meta_title = form.meta_title.data
        settings.meta_description = form.meta_description.data
        settings.meta_keywords = form.meta_keywords.data

        settings.copyright_text = form.copyright_text.data

        # Handle uploads separately
        if isinstance(form.logo.data, FileStorage) and form.logo.data.filename:

            delete_image(settings.logo)

            print("=" * 50)
            print("Logo data:", form.logo.data)
            print("Logo type:", type(form.logo.data))
            print("=" * 50)

            settings.logo = save_image(
                form.logo.data,
                "uploads/site/logos",
                (600, 200)
            )

        if isinstance(form.favicon.data, FileStorage) and form.favicon.data.filename:

            delete_image(settings.favicon)

            settings.favicon = save_image(
                form.favicon.data,
                "uploads/site/favicons",
                (64, 64)
            )

        db.session.commit()

        flash(
            "Settings updated successfully.",
            "success"
        )

        return redirect(url_for("admin.settings"))

    return render_template(
        "admin/settings.html",
        form=form,
        settings=settings
    )