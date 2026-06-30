"""Dashboard Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

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
        render_metric_card("Documents", len(st.session_state.get("uploaded_files", {})), "📚")
    with col2:
        render_metric_card("Total Words", "0", "📝")
    with col3:
        render_metric_card("Chat Messages", "0", "💬")
    with col4:
        render_metric_card("Quizzes", "0", "❓")
    
    st.markdown("---")
    st.subheader("📤 Recent Uploads")
    if not st.session_state.get("uploaded_files"):
        st.info("No documents uploaded yet. Go to 'Upload Notes'!")
    else:
        for name in st.session_state.uploaded_files:
            st.write(f"✅ {name}")

show_dashboard()
