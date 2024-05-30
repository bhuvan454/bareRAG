import os

class Config:
    QDRANT_URL = os.getenv("QDRANT_URL","https://localhost:6333")
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME","ragcollection")


config = Config()