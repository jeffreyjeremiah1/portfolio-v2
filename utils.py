import os
import uuid

from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename

from models import Message


def get_unread_count():
    return Message.query.filter_by(is_read=False).count()


def save_image(image_file, folder, size):
    """
    Save an uploaded image.

    Args:
        image_file: Uploaded file
        folder: Relative folder inside static
                e.g. uploads/profiles
        size: (width, height)

    Returns:
        Relative image path for database storage.
    """

    filename = secure_filename(image_file.filename)

    extension = os.path.splitext(filename)[1].lower()

    new_filename = f"{uuid.uuid4().hex}{extension}"

    upload_folder = os.path.join(
        current_app.static_folder,
        folder
    )

    os.makedirs(upload_folder, exist_ok=True)

    image_path = os.path.join(
        upload_folder,
        new_filename
    )

    image = Image.open(image_file)

    image = image.convert("RGB")

    image.thumbnail(size)

    image.save(
        image_path,
        quality=90
    )

    return f"{folder}/{new_filename}"

def delete_image(image_path):
    """
    Delete an uploaded image except default images.
    """

    if not image_path:
        return

    defaults = {
        "uploads/profiles/default.png",
        "uploads/site/default-logo.png",
        "uploads/site/default-favicon.png",
    }

    if image_path in defaults:
        return

    full_path = os.path.join(
        current_app.static_folder,
        image_path
    )

    if os.path.exists(full_path):
        os.remove(full_path)