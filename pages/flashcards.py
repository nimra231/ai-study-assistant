"""Flashcards Page."""
import sys
import os

# Add project root to Python path (pages run from a different cwd)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

import streamlit as st
from modules.ui_components import render_header, render_info_box
# ... rest of your imports
import streamlit as st
import random
from modules.ui_components import render_header, render_info_box
from modules.flashcard_generator import get_flashcard_generator


def show_flashcards():
    render_header("🎴 Flashcards", "Generate flashcards for quick revision")

    if not st.session_state.get("uploaded_files"):
        render_info_box("📚 Please upload study materials first!", "warning")
        return

    st.subheader("⚙️ Flashcard Settings")
    c1, c2 = st.columns(2)
    with c1:
        num_cards = st.slider("Number of Flashcards", 5, 30, 10)
    with c2:
        topic_focus = st.text_input("🎯 Topic Focus (optional)", placeholder="Leave empty for all topics")

    if st.button("🎴 Generate Flashcards", type="primary", use_container_width=True):
        flashcard_gen = get_flashcard_generator()
        cards = flashcard_gen.generate_flashcards(num_cards, topic_focus)

        if cards:
            if "flashcards" not in st.session_state:
                st.session_state.flashcards = []
            st.session_state.flashcards.extend(cards)
            if "recent_activity" not in st.session_state:
                st.session_state.recent_activity = []
            st.session_state.recent_activity.append(f"Generated {len(cards)} flashcards")
            st.success(f"✅ Generated {len(cards)} flashcards!")
            st.rerun()

    if st.session_state.get("flashcards"):
        st.markdown("---")
        st.subheader("🎴 Your Flashcards")

        study_mode = st.toggle("📖 Study Mode (hide answers)", value=False)

        difficulties = list(set(card.get("difficulty", "Medium") for card in st.session_state.flashcards))
        selected_difficulty = st.multiselect("Filter by Difficulty", difficulties, default=difficulties)

        filtered_cards = [c for c in st.session_state.flashcards if c.get("difficulty", "Medium") in selected_difficulty]

        if not filtered_cards:
            st.info("No flashcards match filters.")
            return

        if "current_card" not in st.session_state:
            st.session_state.current_card = 0

        c1, c2, c3 = st.columns([1, 3, 1])
        with c1:
            if st.button("⬅️ Previous"):
                st.session_state.current_card = (st.session_state.current_card - 1) % len(filtered_cards)
                st.rerun()
        with c3:
            if st.button("Next ➡️"):
                st.session_state.current_card = (st.session_state.current_card + 1) % len(filtered_cards)
                st.rerun()
        with c2:
            st.markdown(f"<p style='text-align:center;'>Card {st.session_state.current_card + 1} of {len(filtered_cards)}</p>", unsafe_allow_html=True)

        card = filtered_cards[st.session_state.current_card]
        st.markdown("---")
        st.markdown(f"<p style='color:#64748b;font-size:0.9rem;'>📂 {card.get('category', 'General')}</p>", unsafe_allow_html=True)
        st.markdown(f"### ❓ {card['question']}")

        if not study_mode:
            st.markdown("---")
            st.markdown(f"### ✅ {card['answer']}")
            if card.get("explanation"):
                st.info(f"💡 {card['explanation']}")
        else:
            with st.expander("Show Answer"):
                st.markdown(f"### ✅ {card['answer']}")
                if card.get("explanation"):
                    st.info(f"💡 {card['explanation']}")

        st.caption(f"Difficulty: {card.get('difficulty', 'Medium')}")

        if st.button("🔀 Shuffle Cards"):
            random.shuffle(filtered_cards)
            st.session_state.current_card = 0
            st.rerun()

        st.markdown("---")
        if st.button("🗑️ Clear All Flashcards"):
            st.session_state.flashcards = []
            st.session_state.current_card = 0
            st.rerun()
