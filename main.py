from backend.apps.rag.services.loadingdata_1 import load_pdf
from backend.apps.rag.services.chunkingdata_2 import split_documents
from backend.apps.rag.services.vectordb_3 import create_database, clear_database
from backend.apps.rag.services.query_database_4 import query_database
from backend.apps.rag.services.llmresponse_5 import query_rag
from typing import List, Dict, Any


import argparse


def main():
    parser = argparse.ArgumentParser(description='this is the rag model')
    parser.add_argument('--load_pdf', type=str, help='load the pdf file and return the text content')

    parser.add_argument('--query_text', type=str, help='query the database')

    parser.add_argument('--debug', action='store_true', help='print debug information')

    
    args = parser.parse_args()
    # print(args)
     
    
    documents_data = load_pdf(args.load_pdf)
    if args.debug:
        print(documents_data)


    split_documents_data = split_documents(documents_data)
    if args.debug:
        print(split_documents_data)

    vector_db = create_database(split_documents_data)

    query_context, prompt = query_database(vector_db, args.query_text)
    if args.debug:
        print(query_context)
        print(prompt)

    rag_response = query_rag(query_context, prompt)
    print(rag_response)


if __name__ == '__main__':
    main()







# from fastapi import APIRouter, File, UploadFile, HTTPException

# router = APIRouter()

# @router.post("/load_pdf/")
# async def load_pdf_file(file: UploadFile = File(...)):
#     """
#     Load the pdf file and return the text content
#     """
#     return load_pdf(file.file)

# @router.post("/split_documents/")
# async def split_documents_api(data: List[Dict[str, Any]]):
#     """
#     Split the documents into chunks
#     """
#     return split_documents(data)

# @router.post("/create_database/")
# async def create_database_api(data: List[Dict[str, Any]]):
#     """
#     Create the database
#     """
#     return create_database(data)

# @router.post("/clear_database/")
# async def clear_database_api():
#     """
#     Clear the database
#     """
#     return clear_database()

# @router.post("/query_database/")
# async def query_database_api(query_text: str):
#     """
#     Query the database
#     """
#     return query_database(query_text)

# @router.post("/query_rag/")

# async def query_rag_api(query_text: str):
#     """
#     Query the RAG model
#     """
#     return query_rag(query_text)
