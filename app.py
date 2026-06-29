"""
AI Study Assistant - Main Application v2
Run with: streamlit run app.py
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from modules.ui_components import apply_custom_styles, render_sidebar, render_footer
from modules.embeddings_manager import get_embeddings_manager

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state="expanded",
)

apply_custom_styles()

def init_session_state():
    for key in config.SESSION_KEYS:
        if key not in st.session_state:
            if key in ["uploaded_files", "chat_history", "quiz_data", "flashcards", "recent_activity"]:
                st.session_state[key] = {}
            elif key == "vector_store":
                st.session_state[key] = None
            elif key in ["summary_data", "study_plan"]:
                st.session_state[key] = {}
            else:
                st.session_state[key] = None

init_session_state()

if st.session_state.vector_store is None:
    embeddings_manager = get_embeddings_manager()
    if embeddings_manager.load_vector_store():
        st.session_state.vector_store = embeddings_manager.vector_store

selected_page = render_sidebar()

if selected_page == "Dashboard":
    from pages.dashboard import show_dashboard
    show_dashboard()
elif selected_page == "Upload Notes":
    from pages.upload_notes import show_upload_notes
    show_upload_notes()
elif selected_page == "AI Tutor":
    from pages.ai_tutor import show_ai_tutor
    show_ai_tutor()
elif selected_page == "Summary":
    from pages.summary import show_summary
    show_summary()
elif selected_page == "Quiz Generator":
    from pages.quiz_generator import show_quiz_generator
    show_quiz_generator()
elif selected_page == "Flashcards":
    from pages.flashcards import show_flashcards
    show_flashcards()
elif selected_page == "Study Planner":
    from pages.study_planner import show_study_planner
    show_study_planner()

render_footer()
