"""
One-off maintenance script: re-sanitizes Project/Post rich-text fields
that were saved before sanitize_html() (utils.py) was wired into the
admin save routes. Safe to re-run — rows that are already clean are
left untouched (and don't get their updated_at bumped).

Usage: venv/bin/python3 sanitize_existing_content.py
"""

from app import app
from models import db, Project, Post
from utils import sanitize_html

RICHTEXT_PROJECT_FIELDS = [
    "description",
    "challenge_text",
    "solution_text",
    "development_process",
    "results_text",
    "lessons_text",
]

with app.app_context():

    changed = 0

    for project in Project.query.all():

        dirty = False

        for field in RICHTEXT_PROJECT_FIELDS:

            original = getattr(project, field)
            cleaned = sanitize_html(original)

            if cleaned != original:
                setattr(project, field, cleaned)
                dirty = True

        if dirty:
            changed += 1
            print(f"Sanitized project #{project.id}: {project.title}")

    for post in Post.query.all():

        original = post.content
        cleaned = sanitize_html(original)

        if cleaned != original:
            post.content = cleaned
            changed += 1
            print(f"Sanitized post #{post.id}: {post.title}")

    if changed:
        db.session.commit()
        print(f"\nDone. {changed} row(s) updated.")
    else:
        print("Nothing to sanitize — all rows already clean.")
