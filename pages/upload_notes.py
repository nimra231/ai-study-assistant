# pages/upload_notes.py
"""Upload Notes Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header, render_info_box
from modules.document_processor import process_uploaded_file

def show_upload_notes():
    render_header("📤 Upload Notes", "Upload your study materials")
    
    st.subheader("📎 Upload New Documents")
    uploaded_files = st.file_uploader(
        "Choose files (PDF, DOCX, PPTX, TXT)",
        type=["pdf", "docx", "pptx", "txt"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        # Initialize if not exists
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = {}
        
        if "processed_files" not in st.session_state:
            st.session_state.processed_files = []
        
        for file in uploaded_files:
            if file.name not in st.session_state.processed_files:
                with st.spinner(f"Processing {file.name}..."):
                    try:
                        # Process the file
                        success = process_uploaded_file(file)
                        if success:
                            st.session_state.uploaded_files[file.name] = {
                                'name': file.name,
                                'size': file.size,
                                'type': file.type,
                                'processed': True
                            }
                            st.session_state.processed_files.append(file.name)
                            st.success(f"✅ Uploaded and processed: {file.name}")
                        else:
                            st.error(f"❌ Failed to process: {file.name}")
                    except Exception as e:
                        st.error(f"❌ Error processing {file.name}: {str(e)}")
        
        # Show uploaded files
        if st.session_state.processed_files:
            st.subheader("📁 Uploaded Documents")
            for filename in st.session_state.processed_files:
                st.write(f"- {filename}")
            
            st.info("✅ Documents ready! You can now use AI Tutor, Summary, Quiz Generator, etc.")
            st.balloons()
    
    # Show current documents status
    if st.session_state.get("processed_files"):
        st.subheader("📊 Document Status")
        st.success(f"✅ {len(st.session_state.processed_files)} documents processed and ready")
    else:
        st.info("📚 No documents uploaded yet")
