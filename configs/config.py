import logging

MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "models/embedding-001"
CHUNK_SIZE = 300 #1-500
CHUNK_OVERLAP = 50

DATA_DIR = r".\Data"
GLOB_PATTERNS = ["*pdf"]

INDEX_NAME = "astro-1"
INDEX_EMBEDDING_SIZE = 768
INDEX_METRIC = "cosine"
INDEX_CLOUD = "aws"
INDEX_REGION = "us-east-1"
VECTOR_STORE_SEARCH_TYPE = "similarity"
NUM_DOCS = 150

LLM_TEMPERATURE = 0.3
LLM_MAX_TOKENS = 500

EPHE_PATH = "utils/sweph/ephe"
USER_DIR = "user_db"
USER_FILE = "users.json"
