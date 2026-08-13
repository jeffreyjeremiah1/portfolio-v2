#!/usr/bin/env python3
"""
Simple database backup script.

Usage:
    python3 scripts/backup_db.py

Dumps the configured database (SQLite or Postgres, whichever
DATABASE_URL points at) to a timestamped file under backups/ (created
if missing, already gitignored). If STORAGE_BACKEND=s3 is configured,
also uploads the dump there under a "backups/" prefix so it survives
even if the local disk is wiped.

This intentionally does not schedule itself — run it on whatever cron
mechanism your host provides (a system crontab, Render/Railway
Cron Jobs, a GitHub Actions schedule with a reachable DB, etc.). Which
one applies depends on where this gets deployed, so it's left as a
manual wiring step rather than guessed at here.
"""

import datetime
import os
import shutil
import sqlite3
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from app import app  # noqa: E402
from models import db  # noqa: E402


BACKUP_DIR = os.path.join(ROOT_DIR, "backups")


def _timestamp():
    return datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")


def backup_sqlite(db_path, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, f"portfolio-{_timestamp()}.db")

    # Use sqlite3's backup API rather than a plain file copy, so a
    # backup taken while the app is mid-write doesn't end up corrupt.
    src_conn = sqlite3.connect(db_path)
    dest_conn = sqlite3.connect(dest)
    with dest_conn:
        src_conn.backup(dest_conn)
    src_conn.close()
    dest_conn.close()

    return dest


def backup_postgres(database_url, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, f"portfolio-{_timestamp()}.sql")

    if shutil.which("pg_dump") is None:
        raise RuntimeError(
            "pg_dump not found on PATH. Install the postgresql-client "
            "package on whatever host/container runs this backup job."
        )

    with open(dest, "wb") as f:
        subprocess.run(["pg_dump", database_url], check=True, stdout=f)

    return dest


def upload_to_s3(local_path):
    from utils import _s3_client

    bucket = app.config.get("S3_BUCKET")
    if not bucket:
        print("STORAGE_BACKEND=s3 but S3_BUCKET is not set — skipping upload.")
        return

    key = f"backups/{os.path.basename(local_path)}"

    with app.app_context():
        _s3_client().upload_file(local_path, bucket, key)

    print(f"Uploaded backup to s3://{bucket}/{key}")


def main():
    with app.app_context():
        db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
        storage_backend = app.config.get("STORAGE_BACKEND")
        # Flask-SQLAlchemy resolves relative sqlite:/// paths against
        # app.instance_path, not the repo root — read the already-resolved
        # absolute path straight from the bound engine instead of
        # re-deriving it (and getting it wrong) here.
        sqlite_path = db.engine.url.database if db_uri.startswith("sqlite:///") else None

    if db_uri.startswith("sqlite:///"):
        dest = backup_sqlite(sqlite_path, BACKUP_DIR)

    elif db_uri.startswith("postgresql://"):
        dest = backup_postgres(db_uri, BACKUP_DIR)

    else:
        print(f"Unsupported DATABASE_URL scheme for backup: {db_uri.split(':', 1)[0]}")
        sys.exit(1)

    print(f"Backup written to {dest}")

    if storage_backend == "s3":
        upload_to_s3(dest)


if __name__ == "__main__":
    main()
