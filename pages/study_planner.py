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
    
    exam_date = st.date_input("Exam Date")
    daily_hours = st.number_input("Daily Study Hours", 1, 12, 2)
    
    if st.button("Create Study Plan"):
        with st.spinner("Creating study plan..."):
            try:
                planner = get_study_planner()
                plan = planner.create_study_plan(exam_date, daily_hours)
                st.markdown(plan)
            except Exception as e:
                st.error(f"Error: {str(e)}")

show_study_planner()
