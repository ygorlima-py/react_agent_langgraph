from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def splitter_documents(documents: list[Document]) -> list[Document]:
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, chunk_overlap=100, add_start_index=True
    )

    return text_splitter.split_documents(documents=documents)
    