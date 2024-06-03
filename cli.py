# from backend.apps.rag.services.loadingdata import load_pdf
# from backend.apps.rag.services.chunkingdata import split_documents
# from backend.apps.rag.services.vectordb import ChromaDB

# from backend.apps.rag.services.query_database import query_database
# from backend.apps.rag.services.llmresponse import query_rag
from backend.apps.rag.config import Config
from backend.apps.rag.utils.chromaDBManager import ChromaDBManager
from backend.apps.rag.utils.embeddingfun import CustomOllamaEmbeddings

# class ChromaDBManager:
#     def __init__(self):
#         self.vector_db = ChromaDB()
#         self.collection = None

#     def get_list_collections(self):
#         return self.vector_db.get_list_collections()

#     def get_collection(self, collection_name: str, embedding_function):
#         return self.vector_db.get_collection(collection_name,CustomOllamaEmbeddings())

#     def initialize_database(self, pdf_path: str, collection_name: str, debug: bool = False):
#         documents_data = load_pdf(pdf_path)
#         if debug:
#             print("Loaded Documents Data:", documents_data)

#         split_documents_data = split_documents(documents_data)
#         if debug:
#             print("Split Documents Data:", split_documents_data)

#         self.collection = self.vector_db.add_collection(collection_name, 
#                                                         CustomOllamaEmbeddings())
#         self.vector_db.add_chunks(split_documents_data)

#         print(f"Collection '{collection_name}' created and data added.")


    
#     def interactive_query(self, collection, debug: bool = False):
#         llm_rag_query  = query_rag("llama3")
#         while True:
#             query_text = input("Enter your query (or 'exit' to quit): ")
#             if query_text.lower() == 'exit':
#                 break

#             query_context, prompt = query_database(collection, query_text)

#             if debug:
#                 print("Query Context:", query_context)
#                 print("Prompt:", prompt)

#             rag_response = llm_rag_query.invoke(query_context, prompt)
#             print("RAG Response:", rag_response)

#     def delete_collection(self, collection_name: str):
#         self.collection = self.vector_db.get_collection(collection_name, CustomOllamaEmbeddings())
#         if self.collection:
#             self.vector_db.chroma_client.delete_collection(collection_name)
#             print(f"Collection '{collection_name}' deleted.")
#         else:
#             print(f"Collection '{collection_name}' not found.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='This is the RAG model cli interface')
    parser.add_argument('--debug', action='store_true', help='Print debug information')
    args = parser.parse_args()

    db_manager = ChromaDBManager()

    while True:
        print("\nOptions:")
        print("1. Load PDF and create collection")
        print("2. Query the database")
        print("3. Delete a specific collection")
        print("4. Exit")

        choice = input("Enter the number of your choice: ")

        if choice == '1':
            pdf_path = input("Enter the path to the PDF file: ")
            collection_name = input("Enter the name of the collection: ")
            db_manager.initialize_database(pdf_path, collection_name, args.debug)

        elif choice == '2':
            print("Available collections:")
            collections_list = db_manager.get_list_collections()
            for collection in collections_list:
                print(collection.name)
            collection_name = input("Enter the name of the collection to query: ")

            if not collection_name:
                print("Collection name cannot be empty.")
                continue
            if collection_name not in [collection.name for collection in collections_list]:
                print(f"Collection '{collection_name}' not found.")
                continue
        
            collection = db_manager.get_collection(collection_name, CustomOllamaEmbeddings())
            if not collection:
                print(f"Collection '{collection_name}' not found.")
                continue

            # db_manager.interactive_query(collection, args.debug)
            query_text = input("Enter your query: ")
            db_manager.query_database(query_text, collection_name, args.debug)


        elif choice == '3':
            collection_name = input("Enter the name of the collection to delete: ")
            db_manager.delete_collection(collection_name)

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice,pick the right option.")


if __name__ == '__main__':
    main()
