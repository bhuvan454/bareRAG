"""
Bhuvan Chennoju
Created Date: 31-05-2024
Description: This file is used to query the RAG model

"""

from langchain_community.llms.ollama import Ollama


def query_rag(query_results, prompt):
    model = Ollama(model="llama3")
    response = model.invoke(prompt)

    sources = [doc.metadata.get("chunk_id") for doc, _score in query_results]

    formated_response = f"Response: {response}\n\nSources: {sources}"
   
    return formated_response