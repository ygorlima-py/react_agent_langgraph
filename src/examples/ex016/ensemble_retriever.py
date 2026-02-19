from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.vectorstores import VectorStoreRetriever
from examples.ex016.pdf_loader import load_documents
from examples.ex016.chroma import load_vector_store
from examples.ex016.retrievers import base_retriever
from examples.ex016.hybrid_search_bm25 import search_bm_25_retriever
from rich import print

# Carregando retriever de vetores
vector_store = load_vector_store()
as_retriever = base_retriever(vector_store=vector_store)

# Carregando retriever do BM 25
documents = load_documents()
bm25_retriever = search_bm_25_retriever(documents=documents)


def ensemble_retriever(as_retriever: VectorStoreRetriever, bm25_retriever: BM25Retriever) -> EnsembleRetriever:
    ensemble_retr = EnsembleRetriever(
        retrievers=[as_retriever, bm25_retriever],
        weights=[0.4, 0.6]
    )
    
    return ensemble_retr

if __name__ == "__main__":
    ensemble_retr = ensemble_retriever(as_retriever=as_retriever, bm25_retriever=bm25_retriever)
    response = ensemble_retr.invoke("Como a olimpo performou nos testes?")
    print(response)