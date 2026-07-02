# pages/flashcards.py
"""Flashcards Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header
from modules.flashcard_generator import get_flashcard_generator

def show_flashcards():
    render_header("🗂️ Flashcards", "Review with flashcards")
    
    # Check if documents exist
    if not st.session_state.get("processed_files"):
        st.warning("📚 Please upload documents first!")
        st.info("Go to 'Upload Notes' to add your study materials.")
        return
    
    # Show document count
    st.success(f"📄 {len(st.session_state.processed_files)} documents loaded")
    
    # Flashcard options
    col1, col2 = st.columns(2)
    with col1:
        num_cards = st.slider("Number of Flashcards", 5, 50, 10)
    with col2:
        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            index=1
        )
    
    # Generate flashcards button
    if st.button("🗂️ Generate Flashcards", type="primary", use_container_width=True):
        with st.spinner("Generating flashcards..."):
            try:
                flashcard_gen = get_flashcard_generator()
                flashcards = flashcard_gen.generate_flashcards(
                    num_cards=num_cards,
                    difficulty=difficulty
                )
                
                if flashcards:
                    st.session_state.flashcards = flashcards
                    st.session_state.flashcard_index = 0
                    st.session_state.show_answer = False
                    st.success(f"✅ Generated {len(flashcards)} flashcards!")
                    st.rerun()
                else:
                    st.warning("No flashcards generated. Please try again.")
            except Exception as e:
                st.error(f"❌ Error generating flashcards: {str(e)}")
    
    # Display flashcards
    if st.session_state.get("flashcards"):
        flashcards = st.session_state.flashcards
        current_idx = st.session_state.get("flashcard_index", 0)
        
        if current_idx < len(flashcards):
            card = flashcards[current_idx]
            
            st.markdown("---")
            st.subheader(f"Flashcard {current_idx + 1} of {len(flashcards)}")
            
            # Show question
            st.markdown("### 📖 Question")
            st.info(card.get('question', ''))
            
            # Show answer
            if st.button("👁️ Show Answer", key="show_answer_btn"):
                st.session_state.show_answer = True
            
            if st.session_state.get("show_answer", False):
                st.markdown("### ✅ Answer")
                st.success(card.get('answer', ''))
                
                # Navigation buttons
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("⬅️ Previous", disabled=current_idx == 0):
                        st.session_state.flashcard_index = current_idx - 1
                        st.session_state.show_answer = False
                        st.rerun()
                with col2:
                    if st.button("🔄 Flip"):
                        st.session_state.show_answer = not st.session_state.show_answer
                        st.rerun()
                with col3:
                    if st.button("Next ➡️", disabled=current_idx == len(flashcards) - 1):
                        st.session_state.flashcard_index = current_idx + 1
                        st.session_state.show_answer = False
                        st.rerun()
            
            # Progress
            st.progress((current_idx + 1) / len(flashcards))
        else:
            st.info("🎉 All flashcards reviewed!")
            if st.button("🔄 Start Over"):
                st.session_state.flashcard_index = 0
                st.session_state.show_answer = False
                st.rerun()
        
        # Reset button
        if st.button("🗑️ Clear Flashcards"):
            st.session_state.flashcards = None
            st.session_state.flashcard_index = 0
            st.session_state.show_answer = False
            st.rerun()
