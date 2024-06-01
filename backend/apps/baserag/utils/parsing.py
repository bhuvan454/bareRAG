
import logging
from typing import List
from langchain.document_loaders.pdf import PyPDFDirectoryLoader


def load_documents(documents_dir):
    print(f"Loading documents from ")
    logging.info(f"Loading documents from {documents_dir}")
    document_loader = PyPDFDirectoryLoader(documents_dir)
    documents = document_loader.load()
    logging.info(f"\nLoaded {len(documents)} documents")
    return documents