

from ollama import embeddings as OllamaEmbeddings


# def get_embedding_function():
#     embeddings = OllamaEmbeddings()
#     return embeddings


class CustomOllamaEmbeddings():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _embed_documents(self, texts):
        embeddings = [
            OllamaEmbeddings(model = 'llama3',prompt = text)['embedding'] for text in texts
        ]
        return embeddings
    
    def __call__(self, input):
        return self._embed_documents(input)
