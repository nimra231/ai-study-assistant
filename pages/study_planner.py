"""Study Planner Page."""
import streamlit as st
from datetime import datetime, timedelta
from modules.ui_components import render_header, render_info_box
from modules.study_planner import get_study_planner
from modules.embeddings_manager import get_embeddings_manager
import config


def show_study_planner():
    render_header("📅 Study Planner", "Create your personalized study schedule")

    if not st.session_state.get("uploaded_files"):
        render_info_box("📚 Please upload study materials first!", "warning")
        return

    st.subheader("⚙️ Plan Settings")
    c1, c2 = st.columns(2)
    with c1:
        exam_date = st.date_input("📅 Exam Date", value=datetime.now() + timedelta(days=14), min_value=datetime.now() + timedelta(days=1))
    with c2:
        daily_hours = st.slider("⏰ Daily Study Hours", min_value=config.MIN_STUDY_HOURS_PER_DAY, max_value=config.MAX_STUDY_HOURS_PER_DAY, value=3)

    study_style = st.select_slider("📊 Study Style", options=["Relaxed", "Balanced", "Intensive"], value="Balanced")
    break_interval = st.slider("☕ Break Interval (minutes)", min_value=25, max_value=90, value=45, step=5)

    embeddings_manager = get_embeddings_manager()
    available_topics = embeddings_manager.get_document_names()
    selected_topics = st.multiselect("📚 Topics to Cover", available_topics, default=available_topics)

    if st.button("📅 Generate Study Plan", type="primary", use_container_width=True):
        planner = get_study_planner()
        exam_datetime = datetime.combine(exam_date, datetime.min.time())
        with st.spinner("Creating your study plan..."):
            plan = planner.create_study_plan(exam_date=exam_datetime, daily_hours=daily_hours, topics=selected_topics, study_style=study_style.lower(), break_interval=break_interval)

        if plan.get("error"):
            st.error(plan["error"])
            return

        st.session_state.study_plan = plan
        if "recent_activity" not in st.session_state:
            st.session_state.recent_activity = []
        st.session_state.recent_activity.append(f"Created study plan for {plan['exam_date']}")
        st.success("✅ Study plan created!")
        st.rerun()

    if st.session_state.get("study_plan"):
        plan = st.session_state.study_plan
        st.markdown("---")
        st.subheader("📋 Plan Overview")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("📅 Exam Date", plan["exam_date"])
        with c2:
            st.metric("📆 Days Left", plan["days_until_exam"])
        with c3:
            st.metric("⏰ Daily Hours", f"{plan['daily_hours']}h")
        with c4:
            st.metric("📚 Total Hours", f"{plan['total_study_hours']}h")

        st.markdown("---")
        st.subheader("📅 Daily Schedule")
        for day in plan["plan"]:
            with st.expander(f"📆 {day['date']} - Day {day['day_number']} - {day['primary_topic']}"):
                st.markdown("**🎯 Goals:**")
                for goal in day["goals"]:
                    st.markdown(f"  • {goal}")
                st.markdown("**⏱️ Study Sessions:**")
                for session in day["sessions"]:
                    st.markdown(f"""
                    <div style="background:#f8fafc;padding:0.8rem;border-radius:8px;margin:0.5rem 0;">
                        <strong>Session {session['session']}</strong> - {session['duration']}<br>
                        📖 {session['activity']}<br>
                        ☕ Break: {session['break_after']}
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")
        plan_text = f"STUDY PLAN\nExam Date: {plan['exam_date']}\nDays: {plan['days_until_exam']}\nDaily Hours: {plan['daily_hours']}\nTotal: {plan['total_study_hours']}h\n\n"
        for day in plan["plan"]:
            plan_text += f"\n{day['date']} - Day {day['day_number']}\nTopic: {day['primary_topic']}\n"
            for goal in day["goals"]:
                plan_text += f"  - {goal}\n"
            for session in day["sessions"]:
                plan_text += f"  Session {session['session']}: {session['duration']} - {session['activity']}\n"

        st.download_button("💾 Download Study Plan", plan_text, file_name=f"study_plan_{plan['exam_date']}.txt")

        if st.button("🗑️ Clear Plan"):
            st.session_state.study_plan = {}
            st.rerun()
