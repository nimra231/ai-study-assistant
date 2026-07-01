"""Summary Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header, render_info_box
from modules.summarizer import get_summarizer

def show_summary():
    render_header("📝 Summary", "Summarize your notes")
    
    if not st.session_state.get("uploaded_files"):
        render_info_box("Upload documents first!", "warning")
        return
    
    summary_type = st.selectbox("Summary Type", ["Concise", "Detailed", "Exam-Focused"])
    
    if st.button("Generate Summary"):
        with st.spinner("Generating summary..."):
            try:
                summarizer = get_summarizer()
                summary = summarizer.generate_summary(summary_type)
                st.markdown(summary)
            except Exception as e:
                st.error(f"Error: {str(e)}")

show_summary()
