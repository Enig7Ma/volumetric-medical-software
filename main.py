import streamlit as st

from app.storage import count_images, ensure_storage


def main() -> None:
    st.set_page_config(page_title="Medical Image Vault", page_icon="🩺", layout="wide")
    ensure_storage()

    st.title("Medical Image Vault")
    st.write(
        "A simple Streamlit app to upload medical images with metadata and search them later."
    )

    st.subheader("Quick links")
    st.page_link("pages/1_Upload.py", label="Go to Upload", icon="⬆️")
    st.page_link("pages/2_Search.py", label="Go to Search", icon="🔎")

    st.subheader("Status")
    st.metric("Uploaded images", count_images())


if __name__ == "__main__":
    main()
