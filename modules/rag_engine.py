"""RAG Engine - Answer questions using retrieved context."""
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chains import RetrievalQA
import config
from modules.embeddings_manager import get_embeddings_manager


class RAGEngine:
    def __init__(self):
        self.llm = None
        self.embeddings_manager = get_embeddings_manager()
        self.qa_chain = None
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

    def _create_qa_chain(self):
        if self.llm is None or self.embeddings_manager.vector_store is None:
            return None
        
        try:
            retriever = self.embeddings_manager.vector_store.as_retriever(search_kwargs={"k": 5})
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )
            return qa_chain
        except Exception as e:
            st.error(f"Error creating QA chain: {str(e)}")
            return None

    def ask(self, question):
        """Ask a question and get an answer based on uploaded documents."""
        if self.llm is None:
            return "LLM not initialized. Check API key."
        
        if self.embeddings_manager.vector_store is None:
            return "No documents uploaded. Please upload documents first."
        
        try:
            qa_chain = self._create_qa_chain()
            if qa_chain is None:
                return "Failed to create QA chain."
            
            result = qa_chain.invoke({"query": question})
            answer = result.get("result", str(result))
            return answer
        except Exception as e:
            return f"Error processing question: {str(e)}"


_rag_engine = None

def get_rag_engine():
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine
