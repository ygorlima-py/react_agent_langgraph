from langchain_chroma import Chroma
from examples.ex015.utils import embeddings_model

def load_vector_stores() -> Chroma:
    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=embeddings_model(),
        persist_directory="./chroma_langchain_db",
    )
    
    return vector_store