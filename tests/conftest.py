from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture()
def isolated_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Force app.storage to use a temp app_data directory for each test."""

    import app.storage as storage

    data_root = tmp_path / "app_data"

    # Patch at the function level so images_dir/db_path pick it up.
    monkeypatch.setattr(storage, "data_dir", lambda: data_root)

    # Ensure directories + DB exist in the temp location.
    storage.ensure_storage()

    return data_root
