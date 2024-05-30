import argparse
import os
import shutil

from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.schema.document import Document

# from generate_embeddings import EmbeddingsGenerator
from generate_embeddings import get_embedding_function
# from langchain.vectorstores.chroma import Chroma
from langchain_community.vectorstores.chroma import Chroma

import logging

CHROMA_PATH = "chroma_db"

def load_documents(documents_dir):
    print(f"Loading documents from ")
    logging.info(f"Loading documents from {documents_dir}")
    document_loader = PyPDFDirectoryLoader(documents_dir)
    documents = document_loader.load()
    logging.info(f"\nLoaded {len(documents)} documents")
    return documents


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


def split_documents(documents: list[Document]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size= 800,
        chunk_overlap= 80,
        length_function= len,
        is_separator_regex = False,
    )
    return splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    db  = Chroma(
        persist_directory =  CHROMA_PATH,
        # embedding_function = EmbeddingsGenerator(embeddings_type="ollama").embedding_function()
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


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("Database cleared")
    else:
        print("No database to clear")

def main():
    CHROMA_PATH = "chroma_db"
    DATA_DIR = "../../data/"

    parser = argparse.ArgumentParser(description="Add documents to the Chroma database")

    parser.add_argument("--reset", action="store_true", help="Clear the database before adding the documents")
    args = parser.parse_args()

    if args.reset:
        clear_database()

    logging.basicConfig(level=logging.INFO)

    documents = load_documents(DATA_DIR)
    chunks = split_documents(documents)
    add_to_chroma(chunks)

if __name__ == "__main__":
    main()