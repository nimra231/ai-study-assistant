"""Quiz Generator Module."""
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from modules.embeddings_manager import get_embeddings_manager
import config


class QuizGenerator:
    def __init__(self):
        self.llm = None
        self.embeddings_manager = get_embeddings_manager()
        self._init_llm()

    def _init_llm(self):
        cfg = config.get_llm_config()
        try:
            if cfg["provider"] == "openai":
                self.llm = ChatOpenAI(api_key=cfg["api_key"], model=cfg["model"], temperature=0.7, max_tokens=2000)
            else:
                self.llm = ChatGoogleGenerativeAI(api_key=cfg["api_key"], model=cfg["model"], temperature=0.7, max_output_tokens=2000)
        except Exception as e:
            st.error(f"Failed to initialize LLM: {str(e)}")

    def _get_context(self, max_chars=10000):
        if self.embeddings_manager.vector_store is None:
            return ""
        all_chunks = []
        for doc_name in self.embeddings_manager.get_document_names():
            results = self.embeddings_manager.search(f"content from {doc_name}", k=8)
            for r in results:
                all_chunks.append(r.page_content if hasattr(r, 'page_content') else str(r))
        context = "\n\n".join(all_chunks)
        return context[:max_chars] + "..." if len(context) > max_chars else context

    def generate_quiz(self, quiz_type, difficulty, num_questions=5):
        if self.llm is None:
            return "LLM not initialized."
        if self.embeddings_manager.vector_store is None:
            return "Upload documents first."

        context = self._get_context()
        if not context:
            return "No content available."

        prompt = f"""Generate {num_questions} {difficulty} {quiz_type} questions based on:

{context}

Format each question clearly with answers."""

        try:
            with st.spinner("Generating quiz..."):
                r = self.llm.invoke(prompt)
                return r.content if hasattr(r, 'content') else str(r)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return ""


_quiz_generator = None

def get_quiz_generator():
    global _quiz_generator
    if _quiz_generator is None:
        _quiz_generator = QuizGenerator()
    return _quiz_generator
