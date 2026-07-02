"""
Configuration module for AI Study Assistant.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# API KEYS & PROVIDERS
# ============================================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ============================================================================
# EMBEDDINGS CONFIGURATION
# ============================================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ============================================================================
# FILE PATHS
# ============================================================================

FAISS_INDEX_PATH = "data/faiss_index"
DOCUMENTS_DB_PATH = "data/documents.json"
VECTOR_STORE_PATH = "data/vector_store"

# ============================================================================
# APP CONFIGURATION
# ============================================================================

APP_TITLE = "AI Study Assistant"
APP_ICON = "🎓"
APP_VERSION = "2.0.0"
PAGE_LAYOUT = "wide"

# ============================================================================
# QUIZ & FLASHCARD CONFIGURATION
# ============================================================================

QUIZ_TYPES = ["Multiple Choice", "True/False", "Short Answer"]
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
SUMMARY_TYPES = ["Concise", "Detailed", "Exam-Focused"]

# ============================================================================
# FILE UPLOAD CONFIGURATION
# ============================================================================

MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".pptx", ".txt"]
MAX_FILES_PER_UPLOAD = 10

# ============================================================================
# SESSION STATE KEYS - COMPLETE LIST
# ============================================================================

SESSION_KEYS = [
    # Document Management
    "uploaded_files",          # Dictionary: {filename: {name, size, type, processed}}
    "processed_files",         # List: [filename1, filename2, ...] - IMPORTANT: Use this to check if documents exist
    "processing_status",       # Dict: {filename: "processing" | "completed" | "failed"}
    
    # Vector Store & RAG
    "vector_store",            # FAISS/Chroma vector store instance
    "embeddings_manager",      # Embeddings manager instance
    "rag_engine",              # RAG engine instance
    
    # Chat & AI Tutor
    "chat_history",            # List: [{role: "user"|"assistant", content: "..."}]
    "chat_session_id",         # String: unique session ID
    
    # Quiz Generator
    "quiz_data",               # List: [{question, options, answer, difficulty}]
    "quiz_answers",            # Dict: {"q_0": "A", "q_1": "B", ...}
    "quiz_score",              # Dict: {"correct": 5, "total": 10, "percentage": 50}
    "quiz_generated",          # Boolean: True if quiz exists
    "quiz_type",               # String: "multiple_choice" | "true_false" | "mixed"
    "quiz_difficulty",         # String: "Easy" | "Medium" | "Hard"
    
    # Flashcards
    "flashcards",              # List: [{question, answer, difficulty, topic}]
    "flashcard_index",         # Integer: current index
    "show_answer",             # Boolean: True if answer shown
    "flashcard_difficulty",    # String: "Easy" | "Medium" | "Hard"
    "flashcard_count",         # Integer: total flashcards
    
    # Summary
    "summary_data",            # Dict: {type, content, generated_at}
    "summary_type",            # String: "Concise" | "Detailed" | "Exam-Focused" | "Bullet Points"
    "summary_length",          # Integer: max length
    
    # Study Planner
    "study_plan",              # Dict: {weekly_schedule, daily_tasks, resources, ...}
    "exam_date",               # Date: exam date
    "study_hours_per_day",     # Float: hours to study per day
    "plan_generated",          # Boolean: True if plan exists
    
    # User Preferences
    "user_preferences",        # Dict: {theme, notifications, default_tab}
    "dark_mode",               # Boolean: True if dark mode enabled
    
    # Activity Tracking
    "recent_activity",         # List: [{action, timestamp, details}]
    "session_start_time",      # DateTime: session start
    "page_visits",             # Dict: {page_name: count}
    
    # Notification
    "notification",            # Dict: {type, message, timestamp}
    
    # Current Page
    "current_page",            # String: current page name
]

# ============================================================================
# NAVIGATION CONFIGURATION
# ============================================================================

PAGES = [
    {"name": "Dashboard", "icon": "🏠", "key": "dashboard"},
    {"name": "Upload Notes", "icon": "📤", "key": "upload_notes"},
    {"name": "AI Tutor", "icon": "🎓", "key": "ai_tutor"},
    {"name": "Summary", "icon": "📝", "key": "summary"},
    {"name": "Quiz Generator", "icon": "📝", "key": "quiz_generator"},
    {"name": "Flashcards", "icon": "🗂️", "key": "flashcards"},
    {"name": "Study Planner", "icon": "📅", "key": "study_planner"},
]

DEFAULT_PAGE = "Dashboard"

# ============================================================================
# MESSAGES
# ============================================================================

MESSAGES = {
    "no_documents": "📚 Please upload study materials first!",
    "go_to_upload": "Go to 'Upload Notes' to add your documents.",
    "documents_loaded": "📄 {count} documents loaded",
    "upload_success": "✅ Uploaded and processed: {filename}",
    "upload_failed": "❌ Failed to process: {filename}",
    "processing": "Processing {filename}...",
    "generating": "Generating {item}...",
    "generated_success": "✅ {item} generated successfully!",
    "generated_failed": "❌ Failed to generate {item}",
}

# ============================================================================
# LLM CONFIGURATION
# ============================================================================

def get_llm_config():
    """Get LLM configuration based on provider."""
    if LLM_PROVIDER == "openai":
        return {
            "provider": "openai", 
            "api_key": OPENAI_API_KEY, 
            "model": OPENAI_MODEL,
            "temperature": 0.7,
            "max_tokens": 2000
        }
    else:
        return {
            "provider": "gemini", 
            "api_key": GOOGLE_API_KEY, 
            "model": GEMINI_MODEL,
            "temperature": 0.7,
            "max_tokens": 2000
        }

# ============================================================================
# API KEY VALIDATION
# ============================================================================

def check_api_keys():
    """Check if API keys are configured properly."""
    if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        return False, "OpenAI API key is missing. Please set OPENAI_API_KEY in .env file."
    elif LLM_PROVIDER == "gemini" and not GOOGLE_API_KEY:
        return False, "Google API key is missing. Please set GOOGLE_API_KEY in .env file."
    return True, "API keys configured successfully."

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize all session state keys with default values."""
    import streamlit as st
    
    for key in SESSION_KEYS:
        if key not in st.session_state:
            # Set default values based on key type
            if key in ["uploaded_files", "chat_history", "quiz_data", 
                       "flashcards", "recent_activity", "page_visits", 
                       "quiz_answers", "quiz_score", "user_preferences",
                       "summary_data", "study_plan", "processing_status"]:
                st.session_state[key] = {}
            elif key == "processed_files":
                st.session_state[key] = []
            elif key in ["vector_store", "embeddings_manager", "rag_engine"]:
                st.session_state[key] = None
            elif key in ["quiz_generated", "show_answer", "dark_mode", 
                        "plan_generated"]:
                st.session_state[key] = False
            elif key == "flashcard_index":
                st.session_state[key] = 0
            elif key in ["quiz_type", "quiz_difficulty", "flashcard_difficulty", 
                        "summary_type", "notification", "current_page", 
                        "chat_session_id"]:
                st.session_state[key] = None
            elif key == "session_start_time":
                from datetime import datetime
                st.session_state[key] = datetime.now()
            elif key in ["summary_length", "flashcard_count"]:
                st.session_state[key] = 0
            elif key in ["exam_date", "study_hours_per_day"]:
                st.session_state[key] = None
            else:
                st.session_state[key] = None

# ============================================================================
# ENVIRONMENT VALIDATION
# ============================================================================

def validate_environment():
    """Validate the environment configuration."""
    issues = []
    
    # Check API keys
    valid, message = check_api_keys()
    if not valid:
        issues.append(message)
    
    # Check data directories
    for path in [FAISS_INDEX_PATH, DOCUMENTS_DB_PATH, VECTOR_STORE_PATH]:
        dir_path = os.path.dirname(path)
        if dir_path and not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create directory {dir_path}: {e}")
    
    return issues

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_page_by_key(key):
    """Get page info by key."""
    for page in PAGES:
        if page["key"] == key:
            return page
    return None

def get_page_names():
    """Get list of page names."""
    return [page["name"] for page in PAGES]

def get_page_keys():
    """Get list of page keys."""
    return [page["key"] for page in PAGES]

# ============================================================================
# EXPOSE CONFIGURATION
# ============================================================================

# Print configuration status when imported
if __name__ == "__main__":
    print("=" * 50)
    print("AI Study Assistant Configuration")
    print("=" * 50)
    print(f"LLM Provider: {LLM_PROVIDER}")
    print(f"Model: {OPENAI_MODEL if LLM_PROVIDER == 'openai' else GEMINI_MODEL}")
    print(f"Embedding Model: {EMBEDDING_MODEL}")
    print(f"Chunk Size: {CHUNK_SIZE}")
    print(f"Chunk Overlap: {CHUNK_OVERLAP}")
    print("-" * 50)
    
    valid, message = check_api_keys()
    if valid:
        print("✅ " + message)
    else:
        print("❌ " + message)
    
    issues = validate_environment()
    if issues:
        print("⚠️ Issues detected:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ Environment configured successfully!")
    
    print("=" * 50)
