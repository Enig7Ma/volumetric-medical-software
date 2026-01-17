from __future__ import annotations

from pathlib import Path

import pytest

from app.storage import (
    _safe_extension,
    count_images,
    delete_image,
    images_dir,
    list_images,
    read_image_bytes,
    save_upload,
    search_images,
)


@pytest.mark.parametrize(
    ("mime", "name", "expected"),
    [
        ("image/jpeg", "x.any", ".jpg"),
        ("image/png", "x.any", ".png"),
        ("image/webp", "x.any", ".webp"),
        (None, "scan.jpeg", ".jpg"),
        (None, "scan.JPG", ".jpg"),
        (None, "scan.png", ".png"),
        (None, "scan.webp", ".webp"),
        (None, "scan.unknown", ".img"),
    ],
)
def test_safe_extension(mime: str | None, name: str, expected: str) -> None:
    assert _safe_extension(mime, name) == expected


def _save(
    *,
    file_bytes: bytes,
    original_name: str,
    medical_case: str,
    description: str,
    tags: list[str],
    mime_type: str | None = None,
) -> int:
    return save_upload(
        file_bytes=file_bytes,
        mime_type=mime_type,
        original_name=original_name,
        medical_case=medical_case,
        description=description,
        tags=tags,
    )


def test_save_upload_creates_file_and_db_record(isolated_storage: Path) -> None:
    before = count_images()

    record_id = _save(
        file_bytes=b"fake-image-bytes",
        mime_type="image/png",
        original_name="image.png",
        medical_case="  Case A  ",
        description="  Desc A  ",
        tags=["CT", "CT", "Neurology"],
    )

    assert record_id > 0
    assert count_images() == before + 1

    records = list_images()
    assert len(records) == 1
    rec = records[0]
    assert rec.id == record_id
    assert rec.original_name == "image.png"
    assert rec.medical_case == "Case A"
    assert rec.description == "Desc A"
    assert rec.tags == ["CT", "Neurology"]
    assert rec.filename.endswith(".png")
    assert rec.uploaded_at

    file_path = images_dir() / rec.filename
    assert file_path.exists()
    assert read_image_bytes(rec.filename) == b"fake-image-bytes"


def test_search_images_filters_case_description_and_tags(
    isolated_storage: Path,
) -> None:
    _save(
        file_bytes=b"a",
        original_name="a.jpg",
        mime_type="image/jpeg",
        medical_case="Stroke follow-up",
        description="MRI of brain",
        tags=["MRI", "Neurology"],
    )
    _save(
        file_bytes=b"b",
        original_name="b.jpg",
        mime_type="image/jpeg",
        medical_case="Chest pain",
        description="X-ray shows mild infiltrate",
        tags=["X-ray", "Emergency"],
    )

    # Case query
    r = search_images(case_query="stroke", description_query="", tags=[])
    assert len(r) == 1
    assert "Stroke" in r[0].medical_case

    # Description query (case-insensitive substring)
    r = search_images(case_query="", description_query="INFILTRATE", tags=[])
    assert len(r) == 1
    assert "infiltrate" in r[0].description.lower()

    # Tags are ANDed (must include all)
    r = search_images(case_query="", description_query="", tags=["MRI", "Neurology"])
    assert len(r) == 1
    assert set(["MRI", "Neurology"]).issubset(set(r[0].tags))

    r = search_images(case_query="", description_query="", tags=["MRI", "Emergency"])
    assert r == []


def test_delete_image_removes_record_and_file(isolated_storage: Path) -> None:
    image_id = _save(
        file_bytes=b"to-delete",
        original_name="del.webp",
        mime_type="image/webp",
        medical_case="Case",
        description="Desc",
        tags=[],
    )

    rec = list_images()[0]
    file_path = images_dir() / rec.filename
    assert file_path.exists()

    assert delete_image(image_id) is True
    assert delete_image(image_id) is False

    assert count_images() == 0
    assert list_images() == []
    assert not file_path.exists()
