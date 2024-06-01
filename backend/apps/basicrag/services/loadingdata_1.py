"""
Bhuvan Chennoju
Created Date: 31-05-2024
Description: This file is used to load and preprocess the files for the rag model

"""

from typing import List, Dict, Any
from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf(file_path: str) -> Dict[str, Any]:
    """
    Load the pdf file and return the text content
    """
    loader = PyMuPDFLoader(file_path)
    return loader.load()
