from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from extensions import limiter
from forms import LoginForm
from models import User, db




auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if user and user.check_password(form.password.data):

            login_user(
                user,
                remember=form.remember.data
            )

            user.last_login = datetime.utcnow()
            db.session.commit()

            flash(
                "Welcome back!",
                "success"
            )

            return redirect(url_for("admin.dashboard"))

        flash(
            "Invalid username or password.",
            "danger"
        )

    return render_template(
        "auth/login.html",
        form=form
    )


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "info"
    )

    return redirect(url_for("auth.login"))