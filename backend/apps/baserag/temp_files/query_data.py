import argparse

# from langchain.vectorstores.chroma import Chroma
from langchain_community.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
# from langchain_coummunity.llms.ollama import Ollama
from langchain_community.llms.ollama import Ollama
# from generate_embeddings import EmbeddingsGenerator
from generate_embeddings import get_embedding_function

CHROMA_PATH = "chroma_db"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

----------------------------------------

Answer the question based on the above context: {question}
"""

def query_rag(query_text: str): 
    db = Chroma(
        persist_directory = CHROMA_PATH,
        # embedding_function = EmbeddingsGenerator().embedding_function()
        embedding_function = get_embedding_function()
    )

    # results 
    results = db.similarity_search_with_score(query_text, 5)

    context_level = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    # prompt = prompt_template.render(context=context_level, question=query_text)
    prompt = prompt_template.format(context=context_level, question=query_text)

    # print(prompt)

    model = Ollama(model="llama3")
    response = model.invoke(prompt)

    sources = [doc.metadata.get("chunk_id") for doc, _score in results]

    foramted_response = f"Response: {response}\n\nSources: {sources}"
    print(foramted_response)
    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query_text", type=str, help = "query text")

    args = parser.parse_args()
    query_text = args.query_text
    response = query_rag(query_text)
    print("Querying RAG")
    print(response)

if __name__ == "__main__":
    main()