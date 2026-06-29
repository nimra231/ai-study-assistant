"""Upload Notes Page."""
import streamlit as st
import os
from modules.ui_components import render_header, render_info_box
from modules.document_processor import process_uploaded_file
from modules.embeddings_manager import get_embeddings_manager
import config


def show_upload_notes():
    render_header("📤 Upload Notes", "Upload your study materials")

    st.subheader("📎 Upload New Documents")
    uploaded_files = st.file_uploader("Drag and drop files", type=["pdf", "docx", "pptx", "txt"], accept_multiple_files=True)

    if uploaded_files:
        embeddings_manager = get_embeddings_manager()
        for uploaded_file in uploaded_files:
            if uploaded_file.name in st.session_state.get("uploaded_files", {}):
                st.warning(f"⚠️ {uploaded_file.name} already uploaded!")
                continue

            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > config.MAX_FILE_SIZE_MB:
                st.error(f"❌ {uploaded_file.name} too large ({file_size_mb:.1f} MB). Max: {config.MAX_FILE_SIZE_MB} MB")
                continue

            file_info = process_uploaded_file(uploaded_file)
            if file_info and file_info.get("text"):
                success = embeddings_manager.add_document(file_info)
                if success:
                    if "uploaded_files" not in st.session_state:
                        st.session_state.uploaded_files = {}
                    st.session_state.uploaded_files[uploaded_file.name] = file_info
                    if "recent_activity" not in st.session_state:
                        st.session_state.recent_activity = []
                    st.session_state.recent_activity.append(f"Uploaded {uploaded_file.name}")
                    st.success(f"✅ {uploaded_file.name} uploaded!")
                else:
                    st.error(f"❌ Failed to process {uploaded_file.name}")

    st.markdown("---")
    st.subheader("📂 Your Documents")
    if st.session_state.get("uploaded_files"):
        search_term = st.text_input("🔍 Search documents", placeholder="Type to search...")
        files = st.session_state.uploaded_files
        if search_term:
            files = {k: v for k, v in files.items() if search_term.lower() in k.lower()}

        for filename, info in files.items():
            with st.expander(f"📄 {filename}"):
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.markdown(f"**Size:** {info.get('size_mb', 0)} MB")
                    st.markdown(f"**Words:** {info.get('word_count', 0):,}")
                with c2:
                    if st.button("👁️ Preview", key=f"preview_{filename}"):
                        st.text_area("Preview", info.get("text", "")[:1000], height=200)
                with c3:
                    if st.button("🗑️ Delete", key=f"delete_{filename}"):
                        embeddings_manager = get_embeddings_manager()
                        if embeddings_manager.remove_document(filename):
                            del st.session_state.uploaded_files[filename]
                            st.session_state.recent_activity.append(f"Deleted {filename}")
                            st.success(f"✅ {filename} deleted!")
                            st.rerun()

        if st.button("🗑️ Clear All Documents", type="secondary"):
            embeddings_manager = get_embeddings_manager()
            embeddings_manager.clear_all()
            st.session_state.uploaded_files = {}
            st.session_state.recent_activity.append("Cleared all documents")
            st.success("✅ All documents cleared!")
            st.rerun()
    else:
        render_info_box("No documents uploaded yet. Upload above!", "info")
