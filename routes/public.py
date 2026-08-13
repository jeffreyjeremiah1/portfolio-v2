from flask import Blueprint, render_template, request, Response
from models import Project
from extensions import limiter
from forms import ContactForm
from models import db, Message, Project, Tag, Testimonial, Post
from flask import flash, redirect, url_for
from notifications import notify_new_message


public = Blueprint("public", __name__)


@public.route("/", methods=["GET", "POST"])
@limiter.limit("5 per hour", methods=["POST"])
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

    testimonials = (
        Testimonial.query
        .filter_by(published=True)
        .order_by(Testimonial.display_order.asc())
        .all()
    )

    if form.validate_on_submit():

        # Honeypot tripped: silently pretend success so the bot doesn't
        # learn its submission was rejected, but never save/notify.
        if form.website.data:
            flash(
                "Message sent successfully!",
                "success"
            )
            return redirect(url_for("public.home"))

        message = Message(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )

        db.session.add(message)
        db.session.commit()

        notify_new_message(message)

        flash(
            "Message sent successfully!",
            "success"
        )

        return redirect(url_for("public.home"))

    return render_template(
        "home.html",
        projects=projects,
        testimonials=testimonials,
        form=form
    )


@public.route("/projects")
def projects_list():

    tag_slug = request.args.get("tag", "").strip()

    search = request.args.get("q", "").strip()

    page = request.args.get("page", 1, type=int)

    query = Project.query.filter_by(published=True)

    if tag_slug:
        query = query.join(Project.tags).filter(Tag.slug == tag_slug)

    if search:
        query = query.filter(
            Project.title.ilike(f"%{search}%") |
            Project.description.ilike(f"%{search}%")
        )

    projects = (
        query
        .order_by(Project.display_order.asc())
        .paginate(
            page=page,
            per_page=6,
            error_out=False
        )
    )

    tags = Tag.query.order_by(Tag.name).all()

    return render_template(
        "projects_list.html",
        projects=projects,
        tags=tags,
        active_tag=tag_slug,
        search=search
    )

@public.route("/projects/<slug>")
def project_detail(slug):

    project = Project.query.filter_by(
        slug=slug,
        published=True
    ).first_or_404()

    project.view_count = (project.view_count or 0) + 1
    db.session.commit()

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


@public.route("/blog")
def blog_list():

    page = request.args.get("page", 1, type=int)

    posts = (
        Post.query
        .filter_by(published=True)
        .order_by(Post.created_at.desc())
        .paginate(
            page=page,
            per_page=6,
            error_out=False
        )
    )

    return render_template(
        "blog_list.html",
        posts=posts
    )


@public.route("/blog/<slug>")
def blog_detail(slug):

    post = Post.query.filter_by(
        slug=slug,
        published=True
    ).first_or_404()

    return render_template(
        "blog_detail.html",
        post=post
    )


@public.route("/robots.txt")
def robots():

    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /login",
        f"Sitemap: {url_for('public.sitemap', _external=True)}",
    ]

    return Response("\n".join(lines), mimetype="text/plain")


@public.route("/sitemap.xml")
def sitemap():

    pages = [
        {"loc": url_for("public.home", _external=True), "priority": "1.0"},
        {"loc": url_for("public.projects_list", _external=True), "priority": "0.8"},
        {"loc": url_for("public.blog_list", _external=True), "priority": "0.6"},
    ]

    projects = Project.query.filter_by(published=True).all()
    for project in projects:
        pages.append({
            "loc": url_for("public.project_detail", slug=project.slug, _external=True),
            "priority": "0.7",
        })

    posts = Post.query.filter_by(published=True).all()
    for post in posts:
        pages.append({
            "loc": url_for("public.blog_detail", slug=post.slug, _external=True),
            "priority": "0.5",
        })

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:
        xml.append("  <url>")
        xml.append(f"    <loc>{page['loc']}</loc>")
        xml.append(f"    <priority>{page['priority']}</priority>")
        xml.append("  </url>")

    xml.append("</urlset>")

    return Response("\n".join(xml), mimetype="application/xml")