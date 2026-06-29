"""Quiz Generator Page."""
import sys
import os

# Add project root to Python path (pages run from a different cwd)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header, render_info_box
# ... rest of your imports
import streamlit as st
from modules.ui_components import render_header, render_info_box
from modules.quiz_generator import get_quiz_generator
import config


def show_quiz_generator():
    render_header("Quiz Generator", "Test your knowledge")

    if not st.session_state.get("uploaded_files"):
        render_info_box("Upload study materials first!", "warning")
        return

    quiz_type = st.selectbox("Question Type", config.QUIZ_TYPES)
    num_questions = st.slider("Number of Questions", 3, 20, 5)
    difficulty = st.selectbox("Difficulty", config.DIFFICULTY_LEVELS)
    topic = st.text_input("Topic Focus (optional)")

    if st.button("Generate Quiz", type="primary"):
        quiz_gen = get_quiz_generator()
        questions = quiz_gen.generate_quiz(quiz_type, num_questions, difficulty, topic)

        if questions:
            if "quiz_data" not in st.session_state:
                st.session_state.quiz_data = []
            st.session_state.quiz_data.append({
                "type": quiz_type,
                "difficulty": difficulty,
                "topic": topic or "All",
                "questions": questions,
            })
            st.success(f"Generated {len(questions)} questions!")
            st.rerun()

    if st.session_state.get("quiz_data"):
        st.subheader("Your Quizzes")
        for quiz in reversed(st.session_state.quiz_data):
            with st.expander(f"{quiz['type']} - {quiz['difficulty']}"):
                for i, q in enumerate(quiz["questions"]):
                    st.write(f"Q{i+1}. {q['question']}")
                    if q.get("options"):
                        for j, opt in enumerate(q["options"]):
                            st.write(f"  {chr(65+j)}. {opt}")
                    with st.expander("Answer"):
                        st.write(f"Correct: {q.get('correct_answer', 'N/A')}")
                        st.write(q.get('explanation', ''))
