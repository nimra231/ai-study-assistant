"""Quiz Generator Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header, render_info_box
from modules.quiz_generator import get_quiz_generator

def show_quiz_generator():
    render_header("❓ Quiz Generator", "Test your knowledge")
    
    if not st.session_state.get("uploaded_files"):
        render_info_box("Upload documents first!", "warning")
        return
    
    try:
        generator = get_quiz_generator()
        st.write("Quiz will appear here!")
    except Exception as e:
        st.error(f"Error: {e}")

show_quiz_generator()
