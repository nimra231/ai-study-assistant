# pages/quiz_generator.py
"""Quiz Generator Page."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header
from modules.quiz_generator import get_quiz_generator

def show_quiz_generator():
    render_header("📝 Quiz Generator", "Test your knowledge")
    
    # Check if documents exist
    if not st.session_state.get("processed_files"):
        st.warning("📚 Please upload documents first!")
        st.info("Go to 'Upload Notes' to add your study materials.")
        return
    
    # Show document count
    st.success(f"📄 {len(st.session_state.processed_files)} documents loaded")
    
    # Quiz options
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.slider("Number of Questions", 1, 20, 5)
    with col2:
        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            index=1
        )
    
    # Quiz type
    quiz_type = st.radio(
        "Quiz Type",
        ["Multiple Choice", "True/False", "Mixed"],
        horizontal=True
    )
    
    # Generate quiz button
    if st.button("🎯 Generate Quiz", type="primary", use_container_width=True):
        with st.spinner("Generating quiz questions..."):
            try:
                quiz_generator = get_quiz_generator()
                questions = quiz_generator.generate_quiz(
                    num_questions=num_questions,
                    difficulty=difficulty,
                    quiz_type=quiz_type
                )
                
                if questions:
                    st.session_state.quiz_data = questions
                    st.success(f"✅ Quiz generated with {len(questions)} questions!")
                    st.rerun()
                else:
                    st.warning("No questions generated. Please try again.")
            except Exception as e:
                st.error(f"❌ Error generating quiz: {str(e)}")
    
    # Display quiz if exists
    if st.session_state.get("quiz_data"):
        st.subheader("📋 Your Quiz")
        
        # Initialize quiz answers if not exists
        if "quiz_answers" not in st.session_state:
            st.session_state.quiz_answers = {}
        
        # Display questions
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"### Question {i+1}")
            st.write(q.get('question', ''))
            
            # Handle different question types
            options = q.get('options', [])
            if options:
                selected = st.radio(
                    f"Select your answer for Q{i+1}",
                    options,
                    key=f"q_{i}",
                    index=None
                )
                if selected:
                    st.session_state.quiz_answers[f"q_{i}"] = selected
            else:
                # Text input for open-ended questions
                answer = st.text_input(
                    f"Your answer for Q{i+1}",
                    key=f"q_text_{i}"
                )
                if answer:
                    st.session_state.quiz_answers[f"q_{i}"] = answer
            
            st.divider()
        
        # Check answers button
        if st.button("✅ Check Answers", type="primary"):
            correct = 0
            total = len(st.session_state.quiz_data)
            
            for i, q in enumerate(st.session_state.quiz_data):
                user_answer = st.session_state.quiz_answers.get(f"q_{i}")
                correct_answer = q.get('answer')
                
                if user_answer == correct_answer:
                    correct += 1
                    st.success(f"Q{i+1}: ✅ Correct!")
                else:
                    st.error(f"Q{i+1}: ❌ Incorrect. Answer: {correct_answer}")
            
            st.info(f"📊 Score: {correct}/{total} ({correct/total*100:.1f}%)")
    
    # Reset quiz button
    if st.session_state.get("quiz_data"):
        if st.button("🔄 Generate New Quiz", use_container_width=True):
            st.session_state.quiz_data = None
            st.session_state.quiz_answers = {}
            st.rerun()
