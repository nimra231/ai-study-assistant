"""Flashcard Generator - Question-Answer cards for revision."""
import json
import re
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import config
from modules.embeddings_manager import get_embeddings_manager


class FlashcardGenerator:
    def __init__(self):
        self.llm = None
        self.embeddings_manager = get_embeddings_manager()
        self._init_llm()

    def _init_llm(self):
        cfg = config.get_llm_config()
        try:
            if cfg["provider"] == "openai":
                self.llm = ChatOpenAI(api_key=cfg["api_key"], model=cfg["model"], temperature=0.7, max_tokens=4000)
            else:
                self.llm = ChatGoogleGenerativeAI(api_key=cfg["api_key"], model=cfg["model"], temperature=0.7, max_output_tokens=4000)
        except Exception as e:
            st.error(f"Failed to initialize LLM: {str(e)}")

    def _get_context(self, num_chunks=8):
        if self.embeddings_manager.vector_store is None:
            return ""
        all_chunks = []
        for doc_name in self.embeddings_manager.get_document_names():
            results = self.embeddings_manager.search(f"key concepts from {doc_name}", k=3)
            for r in results:
                all_chunks.append(r["content"])
        return "\n\n".join(all_chunks[:num_chunks])

    def _extract_json(self, text):
        text = text.replace("```json", "").replace("```", "").strip()
        start = text.find('[')
        end = text.rfind(']')
        if start != -1 and end != -1:
            return text[start:end+1]
        return text

    def generate_flashcards(self, num_cards=10, topic=""):
        context = self._get_context()
        if not context:
            return []

        prompt = f"""Generate {num_cards} flashcards from this material.
{"Focus: " + topic if topic else ""}

{context}

Return JSON array ONLY:
[{{"question":"...","answer":"...","category":"...","difficulty":"Medium"}}]"""

        try:
            with st.spinner(f"Generating {num_cards} flashcards..."):
                r = self.llm.invoke(prompt)
                content = r.content if hasattr(r, 'content') else str(r)
                cards = json.loads(self._extract_json(content))
                for i, c in enumerate(cards):
                    c["id"] = i + 1
                return cards
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return []


_flashcard_generator = None

def get_flashcard_generator():
    global _flashcard_generator
    if _flashcard_generator is None:
        _flashcard_generator = FlashcardGenerator()
    return _flashcard_generator
