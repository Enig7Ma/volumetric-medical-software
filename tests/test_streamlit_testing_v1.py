from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


def _patch_storage_to_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import app.storage as storage

    data_root = tmp_path / "app_data"
    monkeypatch.setattr(storage, "data_dir", lambda: data_root)
    storage.ensure_storage()


def test_main_page_renders_with_empty_storage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_storage_to_tmp(tmp_path, monkeypatch)

    at = AppTest.from_file("main.py").run()

    assert at.title[0].value == "Medical Image Vault"
    assert len(at.metric) == 1
    assert at.metric[0].label == "Uploaded images"
    assert at.metric[0].value == "0"


def test_upload_page_disables_save_without_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_storage_to_tmp(tmp_path, monkeypatch)

    at = AppTest.from_file("pages/1_Upload.py").run()

    assert at.title[0].value == "Upload"
    # Streamlit 1.52 exposes file_uploader as an UnknownElement, so we only assert
    # the form cannot be submitted without a file.
    assert len(at.button) >= 1
    assert at.button[0].label == "Save"
    assert at.button[0].disabled is True

    at = at.text_input[0].set_value("Case A").run()
    at = at.text_area[0].set_value("Description A").run()
    assert at.button[0].disabled is True


def test_search_page_shows_no_results_on_empty_storage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_storage_to_tmp(tmp_path, monkeypatch)

    at = AppTest.from_file("pages/2_Search.py").run()

    assert at.title[0].value == "Search"
    assert at.caption[0].value == "Results: 0"
    assert len(at.info) == 1
    assert at.info[0].value == "No matching uploads found."
