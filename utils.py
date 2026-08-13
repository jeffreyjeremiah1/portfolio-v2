import io
import os
import uuid

from PIL import Image
from flask import current_app, url_for
from werkzeug.utils import secure_filename

from models import Message


def get_unread_count():
    return Message.query.filter_by(is_read=False).count()


def _s3_client():
    import boto3

    return boto3.client(
        "s3",
        region_name=current_app.config.get("S3_REGION"),
        endpoint_url=current_app.config.get("S3_ENDPOINT_URL") or None,
        aws_access_key_id=current_app.config.get("S3_ACCESS_KEY_ID"),
        aws_secret_access_key=current_app.config.get("S3_SECRET_ACCESS_KEY"),
    )


def _using_s3():
    return current_app.config.get("STORAGE_BACKEND") == "s3"


def upload_url(path):
    """
    Build the public URL for a stored upload (image/file) path such as
    "uploads/projects/abc123.jpg". Resolves against S3 when
    STORAGE_BACKEND=s3, otherwise falls back to the local static route.

    Templates should call this instead of url_for('static', filename=...)
    for any *uploaded* (user-controlled) image or file.
    """

    if not path:
        return ""

    if _using_s3():
        base = current_app.config.get("S3_PUBLIC_URL")
        if base:
            return f"{base.rstrip('/')}/{path}"

        bucket = current_app.config.get("S3_BUCKET")
        region = current_app.config.get("S3_REGION")
        if bucket and region:
            return f"https://{bucket}.s3.{region}.amazonaws.com/{path}"

    return url_for("static", filename=path)


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

    image = Image.open(image_file)

    image = image.convert("RGB")

    image.thumbnail(size)

    if _using_s3():
        pil_format = {
            ".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG",
            ".gif": "GIF", ".webp": "WEBP",
        }.get(extension, "JPEG")

        content_type = {
            "JPEG": "image/jpeg", "PNG": "image/png",
            "GIF": "image/gif", "WEBP": "image/webp",
        }[pil_format]

        buffer = io.BytesIO()
        image.save(buffer, format=pil_format, quality=90)
        buffer.seek(0)

        key = f"{folder}/{new_filename}"

        _s3_client().upload_fileobj(
            buffer,
            current_app.config["S3_BUCKET"],
            key,
            ExtraArgs={"ContentType": content_type},
        )

        return key

    upload_folder = os.path.join(
        current_app.static_folder,
        folder
    )

    os.makedirs(upload_folder, exist_ok=True)

    image_path = os.path.join(
        upload_folder,
        new_filename
    )

    image.save(
        image_path,
        quality=90
    )

    return f"{folder}/{new_filename}"


def save_file(file, folder):
    """
    Save an uploaded non-image file (e.g. a PDF resume).

    Args:
        file: Uploaded file
        folder: Relative folder inside static
                e.g. uploads/site/resumes

    Returns:
        Relative file path for database storage.
    """

    filename = secure_filename(file.filename)

    extension = os.path.splitext(filename)[1].lower()

    new_filename = f"{uuid.uuid4().hex}{extension}"

    if _using_s3():
        key = f"{folder}/{new_filename}"

        content_type = "application/pdf" if extension == ".pdf" else "application/octet-stream"

        _s3_client().upload_fileobj(
            file,
            current_app.config["S3_BUCKET"],
            key,
            ExtraArgs={"ContentType": content_type},
        )

        return key

    upload_folder = os.path.join(
        current_app.static_folder,
        folder
    )

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(
        upload_folder,
        new_filename
    )

    file.save(file_path)

    return f"{folder}/{new_filename}"


def delete_image(image_path):
    """
    Delete an uploaded image/file except default images.
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

    if _using_s3():
        try:
            _s3_client().delete_object(
                Bucket=current_app.config["S3_BUCKET"],
                Key=image_path,
            )
        except Exception:
            current_app.logger.exception("Failed to delete S3 object %s", image_path)
        return

    full_path = os.path.join(
        current_app.static_folder,
        image_path
    )

    if os.path.exists(full_path):
        os.remove(full_path)