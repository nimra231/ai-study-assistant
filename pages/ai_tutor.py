"""AI Tutor Page."""
import sys
import os

# FIX: Add project root to Python path for Streamlit Cloud
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header, render_chat_message, render_info_box
from modules.rag_engine import get_rag_engine

def show_ai_tutor():
    render_header("🤖 AI Tutor", "Ask questions about your study materials")

    if not st.session_state.get("uploaded_files"):
        render_info_box("📚 Please upload study materials first!", "warning")
        return

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        role = message.get("role", "user")
        content = message.get("content", "")
        sources = message.get("sources", [])
        render_chat_message(role, content, sources)

    st.markdown("---")
    c1, c2 = st.columns([4, 1])
    with c1:
        user_question = st.text_input("Ask a question...", placeholder="e.g., What are the key concepts in Chapter 3?", key="chat_input")
    with c2:
        ask_button = st.button("🚀 Ask", use_container_width=True, type="primary")

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    if ask_button and user_question:
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        rag_engine = get_rag_engine()
        result = rag_engine.answer_question(user_question)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
            "confidence": result["confidence"],
        })
        if "recent_activity" not in st.session_state:
            st.session_state.recent_activity = []
        st.session_state.recent_activity.append(f"Asked: {user_question[:50]}...")
        st.rerun()

    st.markdown("---")
    st.subheader("💡 Suggested Questions")
    suggestions = ["What are the main topics?", "Explain key concepts", "Important formulas?", "Summarize main arguments", "Exam focus?"]
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                st.session_state.chat_input = suggestion
                st.rerun()
