"""
Shared Flask extension instances that need to be importable from route
modules without causing circular imports with app.py (which creates the
Flask app itself). Each extension is bound to the app via .init_app()
in app.py.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address)
