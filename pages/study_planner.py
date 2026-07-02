# pages/study_planner.py
"""Study Planner Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from datetime import datetime, timedelta
from modules.ui_components import render_header
from modules.study_planner import get_study_planner

def show_study_planner():
    render_header("📅 Study Planner", "Plan your study schedule")
    
    # Check if documents exist
    if not st.session_state.get("processed_files"):
        st.warning("📚 Please upload documents first!")
        st.info("Go to 'Upload Notes' to add your study materials.")
        return
    
    # Show document count
    st.success(f"📄 {len(st.session_state.processed_files)} documents loaded")
    
    # Planner inputs
    col1, col2 = st.columns(2)
    with col1:
        exam_date = st.date_input(
            "📅 Exam Date",
            value=datetime.now() + timedelta(days=30),
            min_value=datetime.now() + timedelta(days=1)
        )
    with col2:
        study_hours_per_day = st.slider(
            "⏰ Hours per Day",
            0.5, 8.0, 2.0, 0.5
        )
    
    # Additional preferences
    with st.expander("⚙️ Study Preferences"):
        preferred_topics = st.text_area(
            "Topics to focus on (optional)",
            placeholder="Enter specific topics you want to focus on..."
        )
        study_time_preference = st.selectbox(
            "Preferred Study Time",
            ["Morning", "Afternoon", "Evening", "Night", "Flexible"]
        )
    
    # Generate plan button
    if st.button("📊 Generate Study Plan", type="primary", use_container_width=True):
        with st.spinner("Creating your personalized study plan..."):
            try:
                planner = get_study_planner()
                study_plan = planner.create_plan(
                    exam_date=exam_date,
                    hours_per_day=study_hours_per_day,
                    topics=preferred_topics if preferred_topics else None
                )
                
                if study_plan:
                    st.session_state.study_plan = study_plan
                    st.success("✅ Study plan created successfully!")
                    st.rerun()
                else:
                    st.warning("Could not create study plan. Please try again.")
            except Exception as e:
                st.error(f"❌ Error creating study plan: {str(e)}")
    
    # Display study plan
    if st.session_state.get("study_plan"):
        plan = st.session_state.study_plan
        
        st.subheader("📋 Your Study Plan")
        
        # Calculate days remaining
        days_remaining = (exam_date - datetime.now().date()).days
        st.metric("Days Until Exam", days_remaining, delta="days left")
        
        # Display plan
        if isinstance(plan, dict):
            # Weekly breakdown
            st.subheader("📅 Weekly Schedule")
            for day, tasks in plan.get('weekly_schedule', {}).items():
                with st.expander(f"📌 {day}"):
                    for task in tasks:
                        st.write(f"- {task}")
            
            # Daily recommendations
            st.subheader("📚 Daily Study Recommendations")
            daily_tasks = plan.get('daily_tasks', [])
            for task in daily_tasks:
                st.checkbox(task)
            
            # Resources
            if 'resources' in plan:
                st.subheader("📖 Recommended Resources")
                for resource in plan['resources']:
                    st.write(f"- {resource}")
        
        # Download plan
        st.download_button(
            label="📥 Download Study Plan",
            data=str(plan),
            file_name="study_plan.txt",
            mime="text/plain"
        )
        
        # Reset button
        if st.button("🔄 Generate New Plan", use_container_width=True):
            st.session_state.study_plan = None
            st.rerun()
    
    # Tips
    with st.expander("💡 Study Tips"):
        st.markdown("""
        **Effective Study Strategies:**
        - 🎯 Set specific, achievable goals for each study session
        - ⏰ Use the Pomodoro Technique (25 min study, 5 min break)
        - 📝 Review material regularly (spaced repetition)
        - 💪 Take breaks to maintain focus
        - 🧠 Test yourself with quizzes and flashcards
        - 📊 Track your progress
        """)
