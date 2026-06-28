"""Embeddings & Vector Store Module - FAISS and text chunking."""
import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document as LangchainDocument
import streamlit as st
import config


class EmbeddingsManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ";", " ", ""]
        )
        self.vector_store = None
        self.documents_db = {}
        self._load_documents_db()

    def _load_documents_db(self):
        if os.path.exists(config.DOCUMENTS_DB_PATH):
            try:
                with open(config.DOCUMENTS_DB_PATH, "r") as f:
                    self.documents_db = json.load(f)
            except Exception:
                self.documents_db = {}

    def _save_documents_db(self):
        os.makedirs(os.path.dirname(config.DOCUMENTS_DB_PATH), exist_ok=True)
        with open(config.DOCUMENTS_DB_PATH, "w") as f:
            json.dump(self.documents_db, f, indent=2)

    def add_document(self, file_info):
        try:
            filename = file_info["filename"]
            text = file_info["text"]

            chunks = self.text_splitter.split_text(text)
            if not chunks:
                st.warning(f"No chunks generated for {filename}")
                return False

            documents = []
            for i, chunk in enumerate(chunks):
                documents.append(LangchainDocument(
                    page_content=chunk,
                    metadata={"source": filename, "chunk_index": i, "total_chunks": len(chunks)}
                ))

            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
            else:
                self.vector_store.add_documents(documents)

            self._save_vector_store()

            self.documents_db[filename] = {
                "filename": filename,
                "size_mb": file_info.get("size_mb", 0),
                "word_count": file_info.get("word_count", 0),
                "char_count": file_info.get("char_count", 0),
                "chunks": len(chunks),
                "extension": file_info.get("extension", ""),
            }
            self._save_documents_db()
            return True

        except Exception as e:
            st.error(f"Error adding document: {str(e)}")
            return False

    def remove_document(self, filename):
        if filename not in self.documents_db:
            return False
        del self.documents_db[filename]
        self._save_documents_db()
        st.warning("Please re-upload remaining documents to rebuild the vector store.")
        return True

    def search(self, query, k=5):
        if self.vector_store is None:
            return []
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return [{"content": doc.page_content, "source": doc.metadata.get("source", "Unknown"),
                     "chunk_index": doc.metadata.get("chunk_index", 0), "score": round(float(score), 4)}
                    for doc, score in results]
        except Exception as e:
            st.error(f"Search error: {str(e)}")
            return []

    def get_document_names(self):
        return list(self.documents_db.keys())

    def _save_vector_store(self):
        if self.vector_store is not None:
            os.makedirs(config.FAISS_INDEX_PATH, exist_ok=True)
            self.vector_store.save_local(config.FAISS_INDEX_PATH)

    def load_vector_store(self):
        try:
            if os.path.exists(config.FAISS_INDEX_PATH):
                self.vector_store = FAISS.load_local(
                    config.FAISS_INDEX_PATH, self.embeddings, allow_dangerous_deserialization=True
                )
                return True
            return False
        except Exception:
            return False

    def clear_all(self):
        self.vector_store = None
        self.documents_db = {}
        if os.path.exists(config.FAISS_INDEX_PATH):
            import shutil
            shutil.rmtree(config.FAISS_INDEX_PATH)
        if os.path.exists(config.DOCUMENTS_DB_PATH):
            os.remove(config.DOCUMENTS_DB_PATH)
        st.success("All documents cleared!")


_embeddings_manager = None

def get_embeddings_manager():
    global _embeddings_manager
    if _embeddings_manager is None:
        _embeddings_manager = EmbeddingsManager()
        _embeddings_manager.load_vector_store()
    return _embeddings_manager
