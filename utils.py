import os
import uuid

from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename

from models import Message


def get_unread_count():
    return Message.query.filter_by(is_read=False).count()


def save_profile_image(image_file):
    """
    Save, resize and return the relative path
    for a profile image.
    """

    filename = secure_filename(image_file.filename)

    extension = os.path.splitext(filename)[1].lower()

    new_filename = f"{uuid.uuid4().hex}{extension}"

    upload_folder = os.path.join(
        current_app.static_folder,
        "uploads",
        "profiles"
    )

    os.makedirs(upload_folder, exist_ok=True)

    image_path = os.path.join(upload_folder, new_filename)

    image = Image.open(image_file)
    image = image.convert("RGB")
    image.thumbnail((300, 300))
    image.save(image_path, quality=90)

    return f"uploads/profiles/{new_filename}"

def delete_profile_image(image_path):
    """
    Delete a profile image unless it's the default.
    """

    if not image_path:
        return

    if image_path == "uploads/profiles/default.png":
        return

    full_path = os.path.join(
        current_app.static_folder,
        image_path
    )

    if os.path.exists(full_path):
        os.remove(full_path)