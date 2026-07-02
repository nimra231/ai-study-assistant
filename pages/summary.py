# pages/summary.py
"""Summary Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header
from modules.summarizer import get_summarizer

def show_summary():
    render_header("📝 Summary", "Summarize your notes")
    
    # Check if documents exist
    if not st.session_state.get("processed_files"):
        st.warning("📚 Please upload documents first!")
        st.info("Go to 'Upload Notes' to add your study materials.")
        return
    
    # Show document count
    st.success(f"📄 {len(st.session_state.processed_files)} documents loaded")
    
    # Summary options
    col1, col2 = st.columns([2, 1])
    with col1:
        summary_type = st.selectbox(
            "Summary Type",
            ["Concise", "Detailed", "Exam-Focused", "Bullet Points"],
            index=0
        )
    with col2:
        max_length = st.slider("Max Length", 100, 1000, 500, 100)
    
    # Generate summary button
    if st.button("📊 Generate Summary", type="primary", use_container_width=True):
        with st.spinner("Generating summary... (This may take a moment)"):
            try:
                summarizer = get_summarizer()
                summary = summarizer.generate_summary(summary_type, max_length)
                
                if summary:
                    st.subheader("📝 Generated Summary")
                    st.markdown(summary)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Summary",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("No summary generated. Please try again.")
            except Exception as e:
                st.error(f"❌ Error generating summary: {str(e)}")
    
    # Quick tips
    with st.expander("💡 Tips for better summaries"):
        st.markdown("""
        - **Concise**: Get a brief overview of the main points
        - **Detailed**: Get an in-depth summary with all key information
        - **Exam-Focused**: Emphasize points likely to appear in exams
        - **Bullet Points**: Get key information in easy-to-digest format
        """)
