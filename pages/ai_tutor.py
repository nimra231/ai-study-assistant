"""AI Tutor Page - TEST."""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

st.title("AI Tutor Test")
st.write("If you see this, imports are working!")

# Test importing modules
try:
    from modules.rag_engine import get_rag_engine
    st.success("rag_engine imported successfully!")
except Exception as e:
    st.error(f"rag_engine import failed: {e}")

try:
    from modules.embeddings_manager import get_embeddings_manager
    st.success("embeddings_manager imported successfully!")
except Exception as e:
    st.error(f"embeddings_manager import failed: {e}")
