from __future__ import annotations

import json
import os
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ImageRecord:
    """A persisted upload and its metadata."""

    id: int
    filename: str
    original_name: str
    medical_case: str
    description: str
    tags: list[str]
    uploaded_at: str


def data_dir() -> Path:
    """Return the base directory for local app data."""
    return Path(__file__).resolve().parent.parent / "app_data"


def images_dir() -> Path:
    """Return the directory where uploaded images are stored."""
    return data_dir() / "images"


def db_path() -> Path:
    """Return the path to the SQLite database file."""
    return data_dir() / "app.db"


def ensure_storage() -> None:
    """Create the storage directories and initialize the database if needed."""
    images_dir().mkdir(parents=True, exist_ok=True)
    data_dir().mkdir(parents=True, exist_ok=True)
    _init_db()


def _connect() -> sqlite3.Connection:
    ensure_storage()
    con = sqlite3.connect(db_path(), check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def _init_db() -> None:
    con = sqlite3.connect(db_path())
    try:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_name TEXT NOT NULL,
                medical_case TEXT NOT NULL,
                description TEXT NOT NULL,
                tags_json TEXT NOT NULL,
                uploaded_at TEXT NOT NULL
            );
            """
        )
        con.commit()
    finally:
        con.close()


def _safe_extension(mime_type: str | None, original_name: str) -> str:
    """Choose a safe image extension from MIME type or file name.

    Falls back to `.img` if the type is unknown.
    """
    if mime_type == "image/jpeg":
        return ".jpg"
    if mime_type == "image/png":
        return ".png"
    if mime_type == "image/webp":
        return ".webp"

    ext = Path(original_name).suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".webp"}:
        return ".jpg" if ext == ".jpeg" else ext

    return ".img"


def save_upload(
    *,
    file_bytes: bytes,
    mime_type: str | None,
    original_name: str,
    medical_case: str,
    description: str,
    tags: list[str],
) -> int:
    """Persist a new upload to disk and store its metadata in SQLite.

    Returns the new database row ID.
    """
    ensure_storage()

    ext = _safe_extension(mime_type, original_name)
    unique_name = f"{uuid.uuid4().hex}{ext}"
    target_path = images_dir() / unique_name

    with open(target_path, "wb") as f:
        f.write(file_bytes)

    uploaded_at = datetime.now(timezone.utc).isoformat()

    con = _connect()
    try:
        cur = con.execute(
            """
            INSERT INTO images (filename, original_name, medical_case, description, tags_json, uploaded_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                unique_name,
                original_name,
                medical_case.strip(),
                description.strip(),
                json.dumps(sorted(set(tags))),
                uploaded_at,
            ),
        )
        con.commit()
        return int(cur.lastrowid)
    finally:
        con.close()


def count_images() -> int:
    """Return the total number of stored uploads."""
    con = _connect()
    try:
        row = con.execute("SELECT COUNT(*) AS c FROM images").fetchone()
        return int(row["c"]) if row else 0
    finally:
        con.close()


def list_images() -> list[ImageRecord]:
    """Return all stored uploads, newest first."""
    con = _connect()
    try:
        rows = con.execute(
            """
            SELECT id, filename, original_name, medical_case, description, tags_json, uploaded_at
            FROM images
            ORDER BY id DESC
            """
        ).fetchall()
        out: list[ImageRecord] = []
        for r in rows:
            out.append(
                ImageRecord(
                    id=int(r["id"]),
                    filename=str(r["filename"]),
                    original_name=str(r["original_name"]),
                    medical_case=str(r["medical_case"]),
                    description=str(r["description"]),
                    tags=list(json.loads(r["tags_json"]) or []),
                    uploaded_at=str(r["uploaded_at"]),
                )
            )
        return out
    finally:
        con.close()


def read_image_bytes(filename: str) -> bytes:
    """Read raw bytes for a stored image file."""
    path = images_dir() / filename
    with open(path, "rb") as f:
        return f.read()


def delete_image(image_id: int) -> bool:
    """Delete an uploaded image and its metadata.

    Returns True if a record existed and was deleted, otherwise False.
    """

    con = _connect()
    try:
        row = con.execute(
            "SELECT filename FROM images WHERE id = ?",
            (int(image_id),),
        ).fetchone()
        if not row:
            return False

        filename = str(row["filename"])
        con.execute("DELETE FROM images WHERE id = ?", (int(image_id),))
        con.commit()
    finally:
        con.close()

    try:
        (images_dir() / filename).unlink(missing_ok=True)
    except Exception:
        # Best-effort cleanup; DB row is already removed.
        pass

    return True


def _contains_all_tags(record_tags: Iterable[str], wanted_tags: set[str]) -> bool:
    if not wanted_tags:
        return True
    record_set = set(record_tags)
    return wanted_tags.issubset(record_set)


def search_images(
    *,
    case_query: str,
    description_query: str,
    tags: list[str],
) -> list[ImageRecord]:
    """Search stored uploads by case/description substrings and tags.

    Tag filtering uses an AND rule: a record must contain all selected tags.
    """
    records = list_images()

    case_q = case_query.strip().lower()
    desc_q = description_query.strip().lower()
    wanted_tags = set(t.strip() for t in tags if t.strip())

    def matches(r: ImageRecord) -> bool:
        if case_q and case_q not in r.medical_case.lower():
            return False
        if desc_q and desc_q not in r.description.lower():
            return False
        if not _contains_all_tags(r.tags, wanted_tags):
            return False
        return True

    return [r for r in records if matches(r)]
