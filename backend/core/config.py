import os
from pathlib import Path
import sys

data_path = Path(__file__).resolve().parents[2] / 'db'

print(data_path)

class Config:
    QDRANT_URL = os.getenv("QDRANT_URL","https://localhost:6333")
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME","ragcollection")
    
    
    DATA_DOC_PATH = os.getenv("DATA_DOC_PATH", os.path.join(data_path, "data"))
    CHROMA_PATH = os.getenv("CHROMA_PATH", os.path.join(data_path, "chroma_db"))




    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "80"))


    RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))

config = Config()