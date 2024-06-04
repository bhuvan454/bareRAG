# LocalRag for Chatting with docuements using Ollama.

This project is about chatting with the docuemnets using LLMs and the RAG techniques. By using the Ollama, and langchain, embedding creation and the chat response generation is done locally using llama3 model. Instead of using the langchain abstraction for every task, I have when with naive chroma client for the vectorstore. 


## File structure

```bash
|----- backend
        | - apps
             | - rag 
                  | - services
                         | - loadingdata_1.py
                         | - chunkingdata_2.py
                         | - vectordb_3.py
                         | - query_database_4.py
                         | - llmresponse_5.py
                  | - utils
                         | - embedding_func.py
                         | - chromaDBManager.py
                  | - config.py
        | - core
             | - config.py


|----- database
        |- docsdata
               | - doc1.pdf
        |- vector_db
               | - collection1
|----- Cli.py 
|----- ragfastapi.py
|----- pyptroject.py
|----- Readme.py
```

## Setup
1. Im using Ollama client to generate the responses for my prompts, so first need to install the Ollama locally and then pull the 'llama3' model.
https://github.com/ollama/ollama
2. Once the Ollama is installed all the depencies for the project can be downloaed with poetry. This will handle all other required packages which includes langchain.

```bash 
poetry install

```
## Run system

I have worked mostly to get the backend up and running, So to use this I have created two scripts, one cli.py for command line interface based, and other ragfastapi.py for the backend endpoints with the fastapi endpoints.

To run the command line interface

```bash

python cli.py

```

to run the fastapi based endpoints

```bash

uvicorn ragfastapi:app --reload

```


## System config

To control the configuration I have created a global config file, which takecares on the database paths, and docuement pasrsing parameters

