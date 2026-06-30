"""Upload Notes Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header, render_info_box

def show_upload_notes():
    render_header("📤 Upload Notes", "Upload your study materials")
    
    st.subheader("📎 Upload New Documents")
    uploaded = st.file_uploader(
        "Choose files (PDF, DOCX, PPTX, TXT)",
        type=["pdf", "docx", "pptx", "txt"],
        accept_multiple_files=True
    )
    
    if uploaded:
        for file in uploaded:
            st.success(f"✅ Uploaded: {file.name}")
            st.session_state.uploaded_files[file.name] = True
        st.info("Documents uploaded! You can now use AI Tutor, Summary, Quiz Generator, etc.")

show_upload_notes()
