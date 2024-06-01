"""
Bhuvan Chennoju
Created Date: 31-05-2024
Description:  This file is used to create the database for the chunks

"""


from langchain_community.vectorstores.chroma import Chroma
from langchain.schema.document import Document
from backend.apps.rag.utils.embeddingfun import get_embedding_function

from backend.apps.rag.config import Config
import os
import shutil






def create_database(chunks: list[Document]):
    db  = Chroma(
        persist_directory =  Config.CHROMA_PATH,
        embedding_function= get_embedding_function()
    )

    # calculate page ids
    chunks_with_ids = calculate_chunk_ids(chunks)

    # add or update the chunks in the chroma db
    existing_items = db.get(include = [])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing items in DB: {len(existing_ids)}")

    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["chunk_id"] not in existing_ids]

    if len(new_chunks):
        print(f"Adding {len(new_chunks)} new items to the DB")
        new_chunk_ids = [chunk.metadata["chunk_id"] for chunk in new_chunks]
        db.add_documents(new_chunks,ids = new_chunk_ids)
        db.persist()

    else:
        print("No new items to add to the DB")
    
    return db


def clear_database():
    if os.path.exists(Config.CHROMA_PATH):
        shutil.rmtree(Config.CHROMA_PATH)
        print("Database cleared")
    else:
        print("No database to clear")



def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        ## if the page id is the same as the last one, increment the index
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # create the chunk id
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # add the chunk id to the metadata
        chunk.metadata["chunk_id"] = chunk_id
    
    return chunks

