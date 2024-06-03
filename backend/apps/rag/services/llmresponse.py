"""
Bhuvan Chennoju
Created Date: 31-05-2024
Description: This file is used to query the RAG model

"""

from langchain_community.llms.ollama import Ollama


class query_rag:
    def __init__(self, model):
        self.model = Ollama(model=model)

    def invoke(self, query_results, prompt):
        response = self.model.invoke(prompt)

        sources = [doc.get('chunk_id') for doc in query_results['metadatas'][0]]
    
        formated_response = f"Response: {response}\n\nSources: {sources}"

        return formated_response
