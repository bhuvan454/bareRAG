"""
Bhuvan Chennoju
Created Date: 31-05-2024
Description: This file is used to split the documents into chunks

"""
from langchain.schema.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.apps.rag.config import Config

def split_documents(documents: list[Document]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size= Config.CHUNK_SIZE,
        chunk_overlap= Config.CHUNK_OVERLAP,
        length_function= len,
        is_separator_regex = False,
    )
    return splitter.split_documents(documents)