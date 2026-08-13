"""
Production WSGI entrypoint.

Run with a real WSGI server, e.g.:
    gunicorn wsgi:app
"""

from app import app

if __name__ == "__main__":
    app.run()
