"""
Bhuvan Chennoju
Created Date: 31-05-2024
Description: This file is used to query the database

"""


from langchain.prompts import ChatPromptTemplate
from backend.apps.rag.config import Config


# from core.config import config

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

----------------------------------------

Answer the question based on the above context: {question}
"""

def query_database(collection, query_text: str):

    # results 
    # results = db.similarity_search_with_score(query_text, int(Config.RAG_TOP_K))
            # Query the collection to get the 5 most relevant results
    results = collection.query(
            query_texts=[query_text], n_results=int(Config.RAG_TOP_K)
            , include=["documents", "metadatas"]
        )

    # context_level = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    context_level = results["documents"][0]

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_level, question=query_text)

    return results, prompt


