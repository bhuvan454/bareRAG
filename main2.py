from backend.apps.rag.services.loadingdata import load_pdf
from backend.apps.rag.services.chunkingdata import split_documents
from backend.apps.rag.services.vectordb import ChromaDB
from backend.apps.rag.utils.embeddingfun import get_embedding_function
from backend.apps.rag.services.query_database import query_database
from backend.apps.rag.services.llmresponse import query_rag
from backend.apps.rag.config import Config
import os
import shutil
from tqdm import tqdm

class ChromaDBManager:
    def __init__(self):
        self.vector_db = ChromaDB()
        self.collection = None

    # initilaizing the database with the pdf files
    def initialize_database(self, pdf_path: str, collection_name: str, debug: bool = False):
        documents_data = load_pdf(pdf_path)
        if debug:
            print("Loaded Documents Data:", documents_data)

        split_documents_data = split_documents(documents_data)
        if debug:
            print("Split Documents Data:", split_documents_data)

        self.collection = self.vector_db.add_collection(collection_name, 
                                                        get_embedding_function)
        self.vector_db.add_chunks(split_documents_data)

        print(f"Collection '{collection_name}' created and data added.")

    # querying the database with the query text
    def interactive_query(self, debug: bool = False):
        if not self.collection:
            print("Please create or load a collection first.")
            return

        while True:
            query_text = input("Enter your query (or 'exit' to quit): ")
            if query_text.lower() == 'exit':
                break

            query_context, prompt = query_database(self.collection, query_text)
            if debug:
                print("Query Context:", query_context)
                print("Prompt:", prompt)

            rag_response = query_rag(query_context, prompt)
            print("RAG Response:", rag_response)

    def clear_database(self):
        if os.path.exists(Config().CHROMA_PATH):
            shutil.rmtree(Config().CHROMA_PATH)
            print("Database cleared.")
        else:
            print("No database to clear.")

    def delete_collection(self, collection_name: str):
        self.collection = self.vector_db.get_collection(collection_name)
        if self.collection:
            self.vector_db.chroma_client.delete_collection(self.collection)
            print(f"Collection '{collection_name}' deleted.")
        else:
            print(f"Collection '{collection_name}' not found.")

#  python main.py --load_pdf '.\db\data\paper.pdf' 
# --query_text 'what is this paper about can you give me the context and why should i care about the paper?'
# 

def main():
    import argparse
    parser = argparse.ArgumentParser(description='This is the RAG model interface')
    parser.add_argument('--debug', action='store_true', help='Print debug information')
    args = parser.parse_args()

    db_manager = ChromaDBManager()

    while True:
        print("\nOptions:")
        print("1. Load PDF and create collection")
        print("2. Query the database")
        print("3. Delete the entire database")
        print("4. Delete a specific collection")
        print("5. Exit")

        choice = input("Enter the number of your choice: ")

        if choice == '1':
            pdf_path = input("Enter the path to the PDF file: ")
            collection_name = input("Enter the name of the collection: ")
            db_manager.initialize_database(pdf_path, collection_name, args.debug)

        elif choice == '2':
            db_manager.interactive_query(args.debug)

        elif choice == '3':
            db_manager.clear_database()

        elif choice == '4':
            collection_name = input("Enter the name of the collection to delete: ")
            db_manager.delete_collection(collection_name)

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()


# run this by 
# python main2.py --debug  or python main2.py