# App Usage

This page describes how to use the **Medical Image Vault** Streamlit app.

## Start the app

From the repo root:

- `streamlit run main.py`

You should see the Home page with quick links to the Upload and Search pages.

## Upload an image

Go to the Upload page (`pages/1_Upload.py`).

1. **Upload an image** using the file picker.
   - Supported formats: PNG, JPG/JPEG, WEBP
2. Fill in **Medical case** (free text).
3. Fill in **Description** (free text).
4. Choose **Tags** from the provided lists (optional).
5. Click **Save**.

After saving, the app shows the assigned **ID** and provides a link to the Search page.

## Search for uploads

Go to the Search page (`pages/2_Search.py`).

In the sidebar filters:

- **Case contains**: substring match (case-insensitive)
- **Description contains**: substring match (case-insensitive)
- **Tags**: select one or more tags

Tag filtering is an AND rule: results must contain **all** selected tags.

Results are displayed as a grid of images. Each result shows:

- Record **ID**
- Original filename
- Case, tags, UTC upload timestamp, and description

## Delete an upload

On the Search results, open **Details** for an item and click **Delete**.

- If the record exists, it is removed from the SQLite database.
- The corresponding stored image file is deleted on a best-effort basis.

## Where data is stored

Uploads are stored locally in:

- `app_data/app.db` (SQLite metadata)
- `app_data/images/` (image files)

## Notes and limitations

- This is a local, file-backed app intended for demos and small-scale usage.
- Search uses in-memory filtering of stored records (fast for small datasets).
- Upload timestamps are stored in UTC.

## Troubleshooting

- If the app starts but shows no pages, verify you’re launching from the repo root.
- If uploads fail, ensure the process has write access to `app_data/`.
