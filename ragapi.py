import json
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from backend.apps.rag.services.loadingdata import load_pdf
from backend.apps.rag.services.chunkingdata import split_documents
from backend.apps.rag.services.vectordb import ChromaDB
from backend.apps.rag.utils.embeddingfun import CustomOllamaEmbeddings
from backend.apps.rag.services.query_database import query_database
from backend.apps.rag.services.llmresponse import query_rag
from backend.apps.rag.config import Config

app = FastAPI()

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDBManager instance
class ChromaDBManager:
    def __init__(self):
        self.vector_db = ChromaDB()
        self.collection = None

    def get_list_collections(self):
        return self.vector_db.get_list_collections()

    def get_collection(self, collection_name: str):
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

db_manager = ChromaDBManager()

class QueryRequest(BaseModel):
    query: str
    collection_name: str

class Message(BaseModel):
    text: str
    sender: str

class Chat(BaseModel):
    collection_name: str
    messages: List[Message]

# In-memory storage for chats (for simplicity, use a database in production)
chat_storage: Dict[str, List[Message]] = {}

CHAT_STORAGE_FILE = Path("chat_storage.json")

def load_chats():
    if CHAT_STORAGE_FILE.exists():
        with open(CHAT_STORAGE_FILE, "r") as file:
            return json.load(file)
    return {}

def save_chats():
    with open(CHAT_STORAGE_FILE, "w") as file:
        json.dump(chat_storage, file)

@app.on_event("startup")
async def startup_event():
    global chat_storage
    chat_storage = load_chats()

@app.on_event("shutdown")
async def shutdown_event():
    save_chats()

@app.post("/upload-pdf/")
async def upload_pdf(collection_name: str, pdf_file: UploadFile = File(...)):
    pdf_path = f"/tmp/{pdf_file.filename}"
    with open(pdf_path, "wb") as buffer:
        buffer.write(pdf_file.file.read())

    # Initialize database with PDF
    db_manager.initialize_database(pdf_path, collection_name, debug=False)
    return {"message": "Collection created and document added successfully"}

@app.post("/query/")
async def query_collection(request: QueryRequest):
    collection = db_manager.get_collection(request.collection_name)

    if not collection:
        return {"error": f"Collection '{request.collection_name}' not found"}

    query_context, prompt = query_database(collection, request.query)
    rag_response = query_rag("llama3").invoke(query_context, prompt)

    # Save the chat
    if request.collection_name not in chat_storage:
        chat_storage[request.collection_name] = []
    chat_storage[request.collection_name].append({"text": request.query, "sender": "user"})
    chat_storage[request.collection_name].append({"text": rag_response, "sender": "bot"})
    save_chats()

    return {"reply": rag_response}

@app.post("/save-chat/")
async def save_chat(chat: Chat):
    chat_storage[chat.collection_name] = [{"text": msg.text, "sender": msg.sender} for msg in chat.messages]
    save_chats()
    return {"message": "Chat saved successfully"}

@app.get("/get-chat/{collection_name}/")
async def get_chat(collection_name: str):
    return {"messages": chat_storage.get(collection_name, [])}

@app.delete("/collection/{collection_name}/")
async def delete_collection(collection_name: str):
    db_manager.delete_collection(collection_name)
    chat_storage.pop(collection_name, None)
    save_chats()
    return {"message": f"Collection '{collection_name}' deleted successfully"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
