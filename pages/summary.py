"""Summary Page."""
import streamlit as st
from modules.ui_components import render_header, render_info_box
from modules.summarizer import get_summarizer
import config


def show_summary():
    render_header("📝 Summary", "Generate summaries from your study materials")

    if not st.session_state.get("uploaded_files"):
        render_info_box("📚 Please upload study materials first!", "warning")
        return

    st.subheader("📋 Choose Summary Type")
    summary_type = st.radio("Summary Type", config.SUMMARY_TYPES, horizontal=True)

    descriptions = {
        "Concise": "Quick overview with key points (best for quick revision)",
        "Detailed": "Comprehensive coverage with explanations (best for deep understanding)",
        "Exam-Focused": "Highlights likely exam content (best for exam prep)",
    }
    st.info(f"**{summary_type}:** {descriptions[summary_type]}")

    if st.button("✨ Generate Summary", type="primary", use_container_width=True):
        summarizer = get_summarizer()
        with st.spinner(f"Generating {summary_type} summary..."):
            summary = summarizer.generate_summary(summary_type)

        st.markdown("---")
        st.subheader(f"📄 {summary_type} Summary")
        st.markdown(summary)

        if "summary_data" not in st.session_state:
            st.session_state.summary_data = {}
        st.session_state.summary_data[summary_type] = summary
        if "recent_activity" not in st.session_state:
            st.session_state.recent_activity = []
        st.session_state.recent_activity.append(f"Generated {summary_type} summary")

        st.download_button("💾 Download Summary", summary, file_name=f"summary_{summary_type.lower().replace(' ', '_')}.txt")

    if st.session_state.get("summary_data"):
        st.markdown("---")
        st.subheader("📚 Previous Summaries")
        for summary_type, content in st.session_state.summary_data.items():
            with st.expander(f"📝 {summary_type}"):
                st.markdown(content)
