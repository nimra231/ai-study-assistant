# pages/ai_tutor.py
"""AI Tutor Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header
from modules.rag_engine import get_rag_engine

def show_ai_tutor():
    render_header("🎓 AI Tutor", "Ask questions about your study materials!")
    
    # Check if documents exist
    if not st.session_state.get("processed_files"):
        st.warning("📚 Please upload study materials first!")
        st.info("Go to 'Upload Notes' to add your documents.")
        return
    
    # Show document count
    st.success(f"📄 {len(st.session_state.processed_files)} documents loaded")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    user_input = st.chat_input("Ask a question about your study materials...")
    if user_input:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get response from RAG engine
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    rag_engine = get_rag_engine()
                    response = rag_engine.ask(user_input)
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
