from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_community.embeddings.ollama import OllamaEmbeddings

from langchain.schema.document import Document

from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings


def get_embedding_function():
    # embeddings = BedrockEmbeddings(
    #     credentials_profile_name="default", region_name="us-east-1"
    # )
    embeddings = OllamaEmbeddings()
    return embeddings

# class EmbeddingsGenerator:
#     def __init__(self, embeddings_type: str):
#         if embeddings_type == 'ollama':
#             self.embeddings = OllamaEmbeddings( model= "llama:7b")
#         elif embeddings_type == 'bedrock':
#             self.embeddings = BedrockEmbeddings(
#                 # credentials=os.environ['BEDROCK_CREDENTIALS'],
#                 # region_name=os.environ['BEDROCK_REGION'],
#                 credentials_profile_name = 'default',
#                 region_name = 'us-west-1'
#             )
#         else:
#             raise ValueError(f'Unknown embeddings type: {embeddings_type}')



#     def embedding_function(self):
#         return self.embeddings 
#     # def getembeddings(self, document: Document):
#     #     return self.embeddings.embed_documents(document)