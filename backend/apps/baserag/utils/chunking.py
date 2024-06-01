from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.schema.document import Document



def split_documents(documents: list[Document], chunk_size: int = 800, chunk_overlap: int = 80):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size= chunk_size,
        chunk_overlap= chunk_overlap,
        length_function= len,
        is_separator_regex = False,
    )
    return splitter.split_documents(documents)


