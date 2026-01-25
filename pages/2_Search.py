"""Streamlit page: search and delete uploaded images."""

import streamlit as st

from app.constants import IMAGING_TAGS, OTHER_TAGS
from app.storage import delete_image, ensure_storage, read_image_bytes, search_images


def main() -> None:
    """Render the Search page."""
    st.set_page_config(page_title="Search", page_icon="🔎", layout="wide")
    ensure_storage()

    st.title("Search")

    with st.sidebar:
        st.subheader("Filters")
        case_query = st.text_input("Case contains")
        description_query = st.text_input("Description contains")
        st.markdown("**Tags**")
        imaging_tag_filter = st.multiselect("Imaging", options=IMAGING_TAGS)
        other_tag_filter = st.multiselect("Other", options=OTHER_TAGS)
        tag_filter = [*imaging_tag_filter, *other_tag_filter]

    results = search_images(
        case_query=case_query,
        description_query=description_query,
        tags=tag_filter,
    )

    st.caption(f"Results: {len(results)}")

    if not results:
        st.info("No matching uploads found.")
        return

    cols = st.columns(3)
    for idx, rec in enumerate(results):
        with cols[idx % 3]:
            st.image(
                read_image_bytes(rec.filename),
                caption=f"ID {rec.id} · {rec.original_name}",
                use_container_width=True,
            )
            with st.expander("Details", expanded=False):
                st.write(f"**Case:** {rec.medical_case}")
                st.write(f"**Tags:** {', '.join(rec.tags) if rec.tags else '—'}")
                st.write(f"**Uploaded (UTC):** {rec.uploaded_at}")
                st.write("**Description:**")
                st.write(rec.description)

                if st.button("Delete", key=f"delete_{rec.id}"):
                    deleted = delete_image(rec.id)
                    if deleted:
                        st.success("Deleted.")
                    else:
                        st.warning("Already deleted.")
                    st.rerun()


if __name__ == "__main__":
    main()
