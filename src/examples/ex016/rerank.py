from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_core.retrievers import BaseRetriever
from langchain_community.document_compressors import FlashrankRerank
from examples.ex016.retrievers import base_retriever
from examples.ex016.chroma import load_vector_store
from examples.ex016.pdf_loader import load_documents
from examples.ex016.hybrid_search_bm25 import search_bm_25_retriever
from examples.ex016.ensemble_retriever import ensemble_retriever
from flashrank import Ranker 
from rich import print


def rerank_retriever(retriever: BaseRetriever):
    '''
    Aqui rerankeamos a busca usando FlashrankRerank e ContextualCompressionRetriever
    cada retriever é como um filtro que ao final no langchain encadeamos esses filtros com
    create_retrieval_chain. No caso do rerank, ele pega o retriever base, ou seja a 
    primeira busca com as_retriever e filtra os 6 primeiros (parametro top_n) que
    mas faz sentido com a pergunta e com os splits
    '''
    compressor = FlashrankRerank(top_n=5)
    
    return ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )
    

if __name__ == "__main__":
    vector_store = load_vector_store()
    documents = load_documents()
    
    as_retriever = base_retriever(vector_store=vector_store)
    bm25_retriever = search_bm_25_retriever(documents=documents)
    
    _ensemble_retriever = ensemble_retriever(as_retriever=as_retriever, bm25_retriever=bm25_retriever)
    
    rerank = rerank_retriever(retriever=_ensemble_retriever)
    
    response = rerank.invoke("O que Produtores tem feito para controlar a anomalia da soja?")
    print(response)