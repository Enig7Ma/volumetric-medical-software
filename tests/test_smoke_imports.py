from __future__ import annotations

import importlib.util
from pathlib import Path


def _import_from_path(module_name: str, path: Path) -> None:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def test_import_main() -> None:
    import main  # noqa: F401


def test_import_pages_by_path() -> None:
    root = Path(__file__).resolve().parent.parent
    _import_from_path("page_upload", root / "pages" / "1_Upload.py")
    _import_from_path("page_search", root / "pages" / "2_Search.py")
