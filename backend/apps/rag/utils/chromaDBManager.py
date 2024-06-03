
from pathlib import Path
import sys
root_path = Path(__file__).resolve().parents[4]
sys.path.append(str(root_path))

from backend.apps.rag.services.loadingdata import load_pdf
from backend.apps.rag.services.chunkingdata import split_documents
from backend.apps.rag.services.vectordb import ChromaDB
from backend.apps.rag.utils.embeddingfun import CustomOllamaEmbeddings
from backend.apps.rag.services.query_database import query_database
from backend.apps.rag.services.llmresponse import query_rag
from backend.apps.rag.config import Config
import json

# Initialize ChromaDBManager instance
class ChromaDBManager:
    def __init__(self):
        self.vector_db = ChromaDB()
        self.collection = None
        self.model = query_rag("llama3")


    def get_list_collections(self):
        return self.vector_db.get_list_collections()

    def get_collection(self, collection_name: str, embedding_function):
        return self.vector_db.get_collection(collection_name, CustomOllamaEmbeddings())

    def initialize_database(self, pdf_path: str, collection_name: str, debug: bool = False):
        documents_data = load_pdf(pdf_path)
        if debug:
            print("Loaded Documents Data:", documents_data)

        split_documents_data = split_documents(documents_data)
        if debug:
            print("Split Documents Data:", split_documents_data)

        self.collection = self.vector_db.add_collection(collection_name, CustomOllamaEmbeddings())
        self.vector_db.add_chunks(split_documents_data)

        print(f"Collection '{collection_name}' created and data added.")

    def delete_collection(self, collection_name: str):
        self.collection = self.vector_db.get_collection(collection_name, CustomOllamaEmbeddings())
        if self.collection:
            self.vector_db.chroma_client.delete_collection(collection_name)
            print(f"Collection '{collection_name}' deleted.")
        else:
            print(f"Collection '{collection_name}' not found.")


    def query_database(self, query_text: str, collection_name: str, debug: bool = False):
        collection = self.get_collection(collection_name, CustomOllamaEmbeddings())
        query_context, prompt = query_database(collection, query_text)

        if debug:
            print("Query Context:", query_context)
            print("Prompt:", prompt)

        rag_response = self.model.invoke(query_context, prompt)
        print("RAG Response:", rag_response)

        return rag_response