"""Summarizer - Concise, Detailed, Exam-Focused summaries."""
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import config
from modules.embeddings_manager import get_embeddings_manager


class Summarizer:
    def __init__(self):
        self.llm = None
        self.embeddings_manager = get_embeddings_manager()
        self._init_llm()

    def _init_llm(self):
        cfg = config.get_llm_config()
        try:
            if cfg["provider"] == "openai":
                self.llm = ChatOpenAI(api_key=cfg["api_key"], model=cfg["model"], temperature=0.3, max_tokens=4000)
            else:
                self.llm = ChatGoogleGenerativeAI(api_key=cfg["api_key"], model=cfg["model"], temperature=0.3, max_output_tokens=4000)
        except Exception as e:
            st.error(f"Failed to initialize LLM: {str(e)}")

    def _get_context(self, max_chars=15000):
        if self.embeddings_manager.vector_store is None:
            return ""
        all_chunks = []
        for doc_name in self.embeddings_manager.get_document_names():
            results = self.embeddings_manager.search(f"content from {doc_name}", k=10)
            for r in results:
                all_chunks.append(r["content"])
        context = "\n\n".join(all_chunks)
        return context[:max_chars] + "..." if len(context) > max_chars else context

    def generate_summary(self, summary_type):
        if self.llm is None:
            return "LLM not initialized."
        if self.embeddings_manager.vector_store is None:
            return "Upload documents first."

        context = self._get_context()
        if not context:
            return "No content available."

        if summary_type == "Concise":
            prompt = f"""Create a CONCISE summary (max 10 bullet points) of:
{context}"""
        elif summary_type == "Detailed":
            prompt = f"""Create a DETAILED summary with headings and explanations of:
{context}"""
        else:
            prompt = f"""Create an EXAM-FOCUSED summary with:
1. Key Concepts
2. Likely Exam Questions
3. Common Mistakes
4. Quick Checklist

Material:
{context}"""

        try:
            with st.spinner(f"Generating {summary_type} summary..."):
                r = self.llm.invoke(prompt)
                return r.content if hasattr(r, 'content') else str(r)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return ""


_summarizer = None

def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = Summarizer()
    return _summarizer
