"""Configuration settings for College PDF Chatbot.

Defines default paths and parameters for RAG pipeline stages.
"""

from pathlib import Path

# Project Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data and Storage Paths
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"

# Chunking Configuration (Stage 3)
DEFAULT_CHUNK_SIZE = 500       # Target characters per text chunk
DEFAULT_CHUNK_OVERLAP = 100    # Overlap characters between consecutive chunks

# Retrieval Configuration (Upcoming Stage 5)
DEFAULT_TOP_K = 3              # Number of relevant chunks retrieved per query

# Model Settings (Upcoming Stage 4 & 6)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "gemini-1.5-flash"
