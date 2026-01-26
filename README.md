# Streamlit Medical Image Vault

## Setup

- `uv sync` or `pip install -e .`

## Run

- From this folder, start the app with:
  - `streamlit run main.py`

## Pages

- Home: `main.py`
- Upload: `pages/1_Upload.py`
- Search: `pages/2_Search.py`

## Data

- Uploads are stored locally in `app_data/` (SQLite database + image files).

## Automatic testing

- Install dev dependencies (once):
  - `uv sync --group dev`
- Run the test suite:
  - `uv run pytest`

The tests include unit tests for the storage layer and lightweight Streamlit UI smoke tests using `streamlit.testing.v1.AppTest`.

## Documentation (Doxygen)

This repo includes a Doxygen setup that generates HTML documentation into `build/docs/html/`.

- Prerequisites:
  - `doxygen` (and optionally `graphviz` for diagrams)
  - On macOS: `brew install doxygen graphviz`
- Generate docs from the repo root:
  - `./scripts/gen_docs.sh`
- View the result:
  - open `build/docs/html/index.html`
