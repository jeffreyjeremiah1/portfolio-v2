from app import app
from models import db, Project

with app.app_context():

    if Project.query.count() == 0:

        project = Project(

            title="Portfolio Website",

            description="Personal portfolio developed using Flask.",

            github="https://github.com/yourusername",

            demo="#",

            image="portfolio.jpg",

            technologies="Flask, Bootstrap, Python"

        )

        db.session.add(project)

        db.session.commit()

        print("Database seeded!")

    else:

        print("Projects already exist.")