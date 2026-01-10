import streamlit as st

from app.constants import IMAGING_TAGS, OTHER_TAGS
from app.storage import ensure_storage, save_upload


def main() -> None:
    st.set_page_config(page_title="Upload", page_icon="⬆️", layout="wide")
    ensure_storage()

    st.title("Upload")

    uploaded = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=False,
    )

    medical_case = st.text_input("Medical case")
    description = st.text_area("Description", height=140)
    st.subheader("Tags")
    imaging_tags = st.multiselect("Imaging", options=IMAGING_TAGS)
    other_tags = st.multiselect("Other", options=OTHER_TAGS)
    tags = [*imaging_tags, *other_tags]

    if uploaded is not None:
        st.subheader("Preview")
        st.image(uploaded.getvalue(), caption=uploaded.name, use_container_width=True)

    can_submit = uploaded is not None and medical_case.strip() and description.strip()

    if st.button("Save", type="primary", disabled=not can_submit):
        record_id = save_upload(
            file_bytes=uploaded.getvalue(),
            mime_type=uploaded.type,
            original_name=uploaded.name,
            medical_case=medical_case,
            description=description,
            tags=tags,
        )
        st.success(f"Saved upload (ID: {record_id}).")
        st.page_link("pages/2_Search.py", label="Go to Search", icon="🔎")


if __name__ == "__main__":
    main()
