from flask import Blueprint, render_template
from models import Project

public = Blueprint("public", __name__)


@public.route("/")
def home():

    projects = Project.query.all()

    return render_template(
        "home.html",
        projects=projects
    )