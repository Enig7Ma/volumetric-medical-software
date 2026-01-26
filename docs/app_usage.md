# App Usage

This page describes how to use the **Medical Image Vault** Streamlit app.

## Home screen

When you open the application, you start on the **Home** page.

Here you can:

- See a short description of the application
- Use quick links to:
  - **Upload** new images
  - **Search** existing images
- View the current number of uploaded images

From this page, you can immediately navigate to the task you want to perform.

## Uploading an image

On the **Upload** page, you can add a new medical image to the vault.

### To upload an image

1. **Select an image**
   - Drag and drop a file into the upload area, or click **Browse files**
   - Supported formats: PNG, JPG, JPEG, WEBP
2. **Enter metadata**
   - **Medical case**: enter a case identifier or name
   - **Description**: enter notes or contextual information about the image
3. **Assign tags** (optional)
   - Select relevant tags under categories such as **Imaging** and **Other**
   - Tags help you organize images and make them easier to find later
4. **Save the image**
   - Click **Save** to upload the image and store all associated metadata

After saving, the image becomes immediately available in the Search view.

Note: the current UI requires both **Medical case** and **Description** to be non-empty before enabling **Save**.

## Searching and filtering images

On the **Search** page, you can browse and locate previously uploaded images.

You can:

- View all uploaded images as thumbnails
- See basic information such as image ID and filename
- Filter results using:
  - Medical case text
  - Description text
  - Tags (for example, imaging modality)

The displayed results update automatically as you adjust the filters.

## Viewing image details

Each image entry includes a **Details** section that you can expand.

In the details view, you can see:

- The medical case name
- Assigned tags
- The upload timestamp (UTC)
- The full description

This allows you to quickly understand the context of an image without opening it separately.

## Managing images

- You can enter full screen mode by clicking the button on the top-right corner of the image.
- If an image is no longer needed, you can delete it directly from the **Details** view by clicking **Delete**.

Deleting permanently removes the image and its metadata from the vault.
