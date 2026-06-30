"""Study Planner Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header, render_info_box
from modules.study_planner import get_study_planner

def show_study_planner():
    render_header("📅 Study Planner", "Plan your study schedule")
    
    if not st.session_state.get("uploaded_files"):
        render_info_box("Upload documents first!", "warning")
        return
    
    try:
        planner = get_study_planner()
        st.write("Study plan will appear here!")
    except Exception as e:
        st.error(f"Error: {e}")

show_study_planner()
