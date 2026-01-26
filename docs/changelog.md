# Changelog

All notable changes to **Medical Image Vault** will be documented in this file.

This project follows a simple versioned history; version numbers come from `pyproject.toml`.

## 0.1.0

Initial release.

### Features

- **Streamlit app with 3 pages**

  - Home page with quick links to Upload and Search (`main.py`)
  - Upload page for saving new images with metadata (`pages/1_Upload.py`)
  - Search page for filtering, viewing, and deleting saved uploads (`pages/2_Search.py`)

- **Upload workflow**

  - Upload a single image file at a time
  - Supported formats: PNG, JPG/JPEG, WEBP
  - Required metadata fields: _Medical case_ and _Description_ (must be non-empty)
  - Optional tag assignment via two tag groups (_Imaging_ and _Other_)
  - Shows an inline preview of the selected image before saving

- **Local persistence (SQLite + filesystem)**

  - Stores metadata in a local SQLite database at `app_data/app.db`
  - Stores image files on disk under `app_data/images/`
  - Generates a unique stored filename per upload (UUID + safe extension)
  - Records an upload timestamp in UTC (ISO-8601)

- **Search and browse**

  - Case-insensitive substring search on _Medical case_
  - Case-insensitive substring search on _Description_
  - Tag filtering with an AND rule (results must contain all selected tags)
  - Results displayed as a grid of image thumbnails with IDs and original filenames
  - Per-result details view showing case, tags, UTC timestamp, and description

- **Delete**

  - Deletes the selected record from SQLite
  - Attempts to delete the stored image file on a best-effort basis

- **Core library module**
  - `app.storage` provides the storage layer: initialize DB/dirs, save uploads, list/search, read image bytes, and delete
  - `app.constants` provides the tag lists used by the UI

### Developer tooling

- **Automated tests**

  - `pytest` unit tests for the storage layer
  - Lightweight Streamlit smoke tests via `streamlit.testing.v1.AppTest`

- **Documentation generation**
  - Doxygen HTML docs generated into `build/docs/html/` via `./scripts/gen_docs.sh`
  - Doc generator inlines the project version (from `uv version --short` when available)
