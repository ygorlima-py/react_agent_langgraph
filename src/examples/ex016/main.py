from examples.ex016.ensemble_retriever import ensemble_retriever
from examples.ex016.retrievers import generate_prompt_template, base_retriever
from examples.ex016.chroma import load_vector_store
from examples.ex016.pdf_loader import load_documents
from examples.ex016.hybrid_search_bm25 import search_bm_25_retriever
from examples.ex016.ensemble_retriever import ensemble_retriever
from examples.ex016.rerank import rerank_retriever
from examples.ex016.utils import Models
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.runnables.base import Runnable
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from dataclasses import dataclass
from rich import print

@dataclass
class RAGPipeline:
    model: Models
    vector_store: Chroma
    documents: list[Document]
    
    def get_retriever(self) -> ContextualCompressionRetriever:
        as_retriever = base_retriever(vector_store=self.vector_store)
        bm25_retriever = search_bm_25_retriever(documents=self.documents)
        _ensemble_retriever = ensemble_retriever(as_retriever=as_retriever, bm25_retriever=bm25_retriever) 
        
        return rerank_retriever(retriever=_ensemble_retriever)
        
    
    def create_chain(self) -> Runnable:
        llm = self.model.llm_model()
        prompt = generate_prompt_template()
        retriever = self.get_retriever()  
        question_answer_chain = create_stuff_documents_chain(llm, prompt)

        return create_retrieval_chain(retriever, question_answer_chain)
    

if __name__ == "__main__":
    
    pipeline = RAGPipeline(model=Models(), vector_store=load_vector_store(), documents=load_documents())
    
    chain = pipeline.create_chain()
    
    response = chain.invoke({"input":"O que Produtores tem feito para controlar a anomalia da soja?"})
    print(response)