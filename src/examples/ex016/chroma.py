from langchain_chroma import Chroma
from langchain_core.documents import Document
from examples.ex016.text_splitter import splitter_documents
from examples.ex016.pdf_loader import load_documents
from examples.ex016.utils import Models
from rich import print




def load_vector_store() -> Chroma:
    '''
    This fuction initializes vector store
    a database for vectors
    
    :return: Return a vectore store 
    :rtype: Chroma
    '''
    
    model = Models()
    vector_store = Chroma(
        collection_name="anomalia_collection",
        embedding_function=model.embedding_model(),
        persist_directory="./chroma_langchain_db",
    )
    
    return vector_store

def generate_ids(splits:list[Document]) -> list[str]:
    '''
    generate ids with metadata informations, source, page_label and
    start_index
    
    :param splits: accept a documents´s list
    :type splits: list[Document]
    :return: a list of id 
    :rtype: list[str]
    '''
    ids = [f"{split.metadata['page_label']}:{split.metadata['start_index']}:{split.metadata['source']}" for split in splits]
    
    return ids

def add_documents_in_vectore_store(documents: list[Document]):
    splits = splitter_documents(documents=documents)
    ids = generate_ids(splits=splits)
    vector_store = load_vector_store()
    return vector_store.add_documents(documents=splits, ids=ids)




if __name__ == "__main__":
    documents = load_documents()
    result = add_documents_in_vectore_store(documents=documents)
  