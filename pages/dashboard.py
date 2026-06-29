"""Dashboard Page."""
import sys
import os

# Add project root to Python path (pages run from a different cwd)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header, render_info_box
# ... rest of your imports
import streamlit as st
from modules.ui_components import render_header, render_metric_card, render_info_box


def show_dashboard():
    render_header("🏠 Dashboard", "Your study command center")

    from config import check_api_keys
    is_valid, msg = check_api_keys()
    if not is_valid:
        render_info_box(f"⚠️ {msg}", "warning")
        st.info("Add API keys in Streamlit Cloud Secrets.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        num_docs = len(st.session_state.get("uploaded_files", {}))
        render_metric_card("Documents", str(num_docs), "📚")
    with col2:
        total_words = sum(f.get("word_count", 0) for f in st.session_state.get("uploaded_files", {}).values())
        render_metric_card("Total Words", f"{total_words:,}", "📝")
    with col3:
        chat_count = len(st.session_state.get("chat_history", []))
        render_metric_card("Chat Messages", str(chat_count), "💬")
    with col4:
        quiz_count = len(st.session_state.get("quiz_data", []))
        render_metric_card("Quizzes", str(quiz_count), "❓")

    st.markdown("---")
    st.subheader("📤 Recent Uploads")
    if st.session_state.get("uploaded_files"):
        for filename, info in list(st.session_state.uploaded_files.items())[-5:]:
            ext = info.get("extension", "").replace(".", "").upper()
            icon = {"PDF": "📄", "DOCX": "📝", "PPTX": "📊", "TXT": "📃"}.get(ext, "📄")
            st.markdown(f"**{icon} {filename}** - {info.get('word_count', 0):,} words")
    else:
        render_info_box("No documents uploaded yet. Go to 'Upload Notes'!", "info")

    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📤 Upload Notes", use_container_width=True):
            st.session_state.current_page = "Upload Notes"
            st.rerun()
    with c2:
        if st.button("🤖 Ask AI Tutor", use_container_width=True):
            st.session_state.current_page = "AI Tutor"
            st.rerun()
    with c3:
        if st.button("❓ Generate Quiz", use_container_width=True):
            st.session_state.current_page = "Quiz Generator"
            st.rerun()
