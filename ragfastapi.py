from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.apps.rag.utils.chromaDBManager import ChromaDBManager
from backend.apps.rag.config import Config
from typing import List, Dict
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



db_manager = ChromaDBManager()


# defining models and the API endpoints
class QueryRequest(BaseModel):
    query: str
    collection_name: str

class Message(BaseModel):
    text: str
    sender: str

class Chat(BaseModel):
    collection_name: str
    messages: List[Message]

@app.post("/chat/{session_name}/")
async def chat(session_name: str):
    chat_json_path = f"{Config.DATA_CHAT_PATH}/user_chat/{session_name}.json"
    if not os.path.exists(chat_json_path):
        return {"message": "Chat not found"}
    return {"message": "Chat found"}

@app.post("/chat/{session_name}/store/")
async def store_chat(session_name: str, chat: Chat):
    chat_json_path = f"{Config.DATA_CHAT_PATH}/user_chat/{session_name}.json"
    with open(chat_json_path, "w") as buffer:
        json.dump(chat.dict(), buffer)
    return {"message": "Chat stored successfully"}

@app.get("/chat/{session_name}/")
async def get_chat(session_name: str):
    chat_json_path = f"{Config.DATA_CHAT_PATH}/user_chat/{session_name}.json"
    if not os.path.exists(chat_json_path):
        return {"message": "Chat not found"}
    with open(chat_json_path, "r") as buffer:
        chat = Chat(**json.load(buffer))
    return chat

@app.delete("/chat/{session_name}/")
async def delete_chat(session_name: str):
    chat_json_path = f"{Config.DATA_CHAT_PATH}/user_chat/{session_name}.json"
    if not os.path.exists(chat_json_path):
        return {"message": "Chat not found"}
    os.remove(chat_json_path)
    return {"message": "Chat deleted successfully"}

@app.get("/chat/")
async def list_chats():
    chat_files = os.listdir(f"{Config.DATA_CHAT_PATH}/user_chat/")
    return {"chats": chat_files}



@app.get("/collections/")
async def list_collections():
    return db_manager.get_list_collections()

@app.post("/upload-pdf/")
async def upload_pdf(collection_name: str, pdf_file: UploadFile = File(...)):
    pdf_path = f"{Config.DATA_DOC_PATH}/{pdf_file.filename}"
    with open(pdf_path, "wb") as buffer:
        buffer.write(pdf_file.file.read())

    db_manager.initialize_database(pdf_path, collection_name, debug=False)
    return {"message": "collection creaed and document added successfully"}

@app.post("/query/")
async def llm_response(request: QueryRequest):
    rag_response = db_manager.query_database(request.query, request.collection_name)
    return {"reply": rag_response}
    
@app.delete("/collection/{collection_name}/")
async def delete_collection(collection_name: str):
    db_manager.delete_collection(collection_name)
    return {"message": f"Collection '{collection_name}' deleted successfully"}
