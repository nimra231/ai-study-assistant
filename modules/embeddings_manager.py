"""Embeddings Manager Module."""
import os
import json
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Config
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_STORE_PATH = "data/faiss_index"
DOCUMENTS_DB_PATH = "data/documents.json"


class EmbeddingsManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vector_store = None
        self._documents = {}
        self._load_documents_db()
    
    def _load_documents_db(self):
        """Load documents database."""
        if os.path.exists(DOCUMENTS_DB_PATH):
            try:
                with open(DOCUMENTS_DB_PATH, 'r') as f:
                    self._documents = json.load(f)
            except:
                self._documents = {}
        else:
            self._documents = {}
    
    def _save_documents_db(self):
        """Save documents database."""
        os.makedirs(os.path.dirname(DOCUMENTS_DB_PATH), exist_ok=True)
        with open(DOCUMENTS_DB_PATH, 'w') as f:
            json.dump(self._documents, f)
    
    def add_document(self, name, content, chunks):
        """Add document to database."""
        self._documents[name] = {
            "content": content,
            "chunks": len(chunks)
        }
        self._save_documents_db()
    
    def get_document_names(self):
        """Get list of document names."""
        return list(self._documents.keys())
    
    def load_vector_store(self):
        """Load existing vector store from disk."""
        if os.path.exists(VECTOR_STORE_PATH):
            try:
                self.vector_store = FAISS.load_local(
                    VECTOR_STORE_PATH, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                return True
            except Exception as e:
                st.error(f"Error loading vector store: {e}")
                return False
        return False
    
    def save_vector_store(self):
        """Save vector store to disk."""
        if self.vector_store:
            os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)
            self.vector_store.save_local(VECTOR_STORE_PATH)
    
    def create_vector_store(self, documents):
        """Create new vector store from documents."""
        os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        self.save_vector_store()
        return self.vector_store
    
    def add_documents(self, documents):
        """Add documents to existing vector store."""
        if self.vector_store is None:
            return self.create_vector_store(documents)
        self.vector_store.add_documents(documents)
        self.save_vector_store()
        return self.vector_store
    
    def similarity_search(self, query, k=5):
        """Search for similar documents."""
        if self.vector_store is None:
            return []
        return self.vector_store.similarity_search(query, k=k)
    
    def search(self, query, k=5):
        """Alias for similarity_search."""
        return self.similarity_search(query, k=k)


def get_embeddings_manager():
    """Factory function to get embeddings manager instance."""
    return EmbeddingsManager()
