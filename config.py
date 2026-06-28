"""
Configuration module for AI Study Assistant.
"""
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

FAISS_INDEX_PATH = "data/faiss_index"
DOCUMENTS_DB_PATH = "data/documents.json"

APP_TITLE = "AI Study Assistant"
APP_ICON = "🎓"
PAGE_LAYOUT = "wide"

QUIZ_TYPES = ["Multiple Choice", "True/False", "Short Answer"]
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
SUMMARY_TYPES = ["Concise", "Detailed", "Exam-Focused"]

MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".pptx", ".txt"]

SESSION_KEYS = [
    "uploaded_files", "chat_history", "vector_store",
    "current_page", "quiz_data", "flashcards",
    "study_plan", "summary_data", "recent_activity",
]


def get_llm_config():
    if LLM_PROVIDER == "openai":
        return {"provider": "openai", "api_key": OPENAI_API_KEY, "model": OPENAI_MODEL}
    else:
        return {"provider": "gemini", "api_key": GOOGLE_API_KEY, "model": GEMINI_MODEL}


def check_api_keys():
    if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        return False, "OpenAI API key is missing."
    elif LLM_PROVIDER == "gemini" and not GOOGLE_API_KEY:
        return False, "Google API key is missing."
    return True, "API keys configured successfully."
