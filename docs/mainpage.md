# Medical Image Vault – Developer Documentation

This documentation is generated with **Doxygen** from the Python source code.

The documentation header displays the current project version (taken from `uv version --short` when you run the docs generator).

## Project overview

A small Streamlit app that lets you:

- Upload medical images (with case name, description, and tags)
- Persist metadata in SQLite and store images on disk
- Search and delete uploads

## Entry points

- Home page: `main.py`
- Upload page: `pages/1_Upload.py`
- Search page: `pages/2_Search.py`

## Core modules

- `app.storage`: SQLite + file storage for uploads
- `app.constants`: Tag lists used by the UI

## App usage

- See the user-facing walkthrough in [App Usage](docs/app_usage.md).

## Build the docs

On macOS (Homebrew):

- `brew install doxygen graphviz`
- From the repo root: `./scripts/gen_docs.sh`

The generated site will be written to `build/docs/html/index.html`.
