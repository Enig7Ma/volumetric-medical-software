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
