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
    
    # Initialize processed_files if not exists
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = []
    
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = {}
    
    if uploaded:
        for file in uploaded:
            # Check if already processed
            if file.name not in st.session_state.processed_files:
                st.success(f"✅ Uploaded: {file.name}")
                st.session_state.uploaded_files[file.name] = True
                # CRITICAL: Add to processed_files list
                st.session_state.processed_files.append(file.name)
        
        st.info("Documents uploaded! You can now use AI Tutor, Summary, Quiz Generator, etc.")
    
    # Show current uploaded files
    if st.session_state.processed_files:
        st.subheader("📁 Uploaded Documents")
        for filename in st.session_state.processed_files:
            st.write(f"- {filename}")
        st.success(f"✅ {len(st.session_state.processed_files)} documents ready")

show_upload_notes()
