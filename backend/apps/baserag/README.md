so the file sturcture i need is important



RAG ----------------------------- 
------ document ---> parse the docuemnt ----> chunk the document ------> vectorstore with embedding functions and update logic -----> store the embeddings 

user -----> query ----> embedding function ----> embeddings -------> semantic search ----->  ranking ------> final context


final context --------> send to llm with insturctions -----> geneartion of the answers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'




Now for getting this functionality I need the backend infrastructure.....which including somehow handing the data parsing, chunking the documents with different structures, some kind of vecotorstore backend, and embedding generator.


1) lets start with the docuement parser. to get the most out of the document, I want to use a fancy or some advanced way of extracting the content lik use OCR or NER this will help populate some metedata about the document as well. 