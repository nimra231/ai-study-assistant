"""AI Tutor Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.rag_engine import get_rag_engine

def show_ai_tutor():
    st.title("🎓 AI Tutor")
    st.write("Ask questions about your study materials!")
    
    if not st.session_state.get("uploaded_files"):
        st.warning("📚 Please upload study materials first!")
        return
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    user_input = st.chat_input("Ask a question...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get response from RAG engine
        try:
            rag_engine = get_rag_engine()
            response = rag_engine.ask(user_input)
            
            with st.chat_message("assistant"):
                st.write(response)
            
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {str(e)}")

show_ai_tutor()
