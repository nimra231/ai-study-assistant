"""RAG Engine - Answer questions using retrieved context."""
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import config
from modules.embeddings_manager import get_embeddings_manager


class RAGEngine:
    def __init__(self):
        self.llm = None
        self.embeddings_manager = get_embeddings_manager()
        self._init_llm()

    def _init_llm(self):
        cfg = config.get_llm_config()
        try:
            if cfg["provider"] == "openai":
                self.llm = ChatOpenAI(api_key=cfg["api_key"], model=cfg["model"], temperature=0.3, max_tokens=2000)
            else:
                self.llm = ChatGoogleGenerativeAI(api_key=cfg["api_key"], model=cfg["model"], temperature=0.3, max_output_tokens=2000)
        except Exception as e:
            st.error(f"Failed to initialize LLM: {str(e)}")

    def answer_question(self, question):
        if self.llm is None:
            return {"answer": "LLM not initialized. Check API keys.", "sources": [], "confidence": 0}
        if self.embeddings_manager.vector_store is None:
            return {"answer": "No documents uploaded. Go to Upload Notes first.", "sources": [], "confidence": 0}

        try:
            with st.spinner("Searching your notes..."):
                docs = self.embeddings_manager.search(question, k=5)

            if not docs:
                return {"answer": "No relevant info found in your notes.", "sources": [], "confidence": 0}

            context = "\n\n".join([f"[From: {d['source']}]\n{d['content']}" for d in docs])

            prompt = f"""You are an AI Study Assistant. Answer ONLY from the context below.
If the answer is not in the context, say: "I could not find this in your uploaded notes."

Context:
{context}

Question: {question}

Answer:"""

            with st.spinner("Generating answer..."):
                response = self.llm.invoke(prompt)
                answer = response.content if hasattr(response, 'content') else str(response)

            avg_score = sum(d["score"] for d in docs) / len(docs)
            confidence = min(100, max(0, round((1 - avg_score) * 100, 1)))
            sources = list(set([d["source"] for d in docs]))

            return {"answer": answer, "sources": sources, "confidence": confidence, "retrieved_chunks": len(docs)}

        except Exception as e:
            return {"answer": f"Error: {str(e)}", "sources": [], "confidence": 0}


_rag_engine = None

def get_rag_engine():
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine
