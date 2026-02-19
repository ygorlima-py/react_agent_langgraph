from examples.ex016.chroma import load_vector_store
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_chroma import Chroma
from examples.ex016.utils import Models
from examples.ex016.system_prompt import SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from rich import print


def base_retriever(vector_store: Chroma) -> VectorStoreRetriever:
    retriever = vector_store.as_retriever(
        search_type="mmr", search_kwargs={"k": 35, "fetch_k": 60, "lambda_mult": 0.5}
    )

    return retriever

def generate_prompt_template() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(   
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}")
        ]
    )
    
    return prompt

if __name__ == '__main__':
    vector_store = load_vector_store()
    retriever = base_retriever(vector_store=vector_store)
    docs = retriever.invoke('Olimpo')
    
    for doc in docs: 
        print(f'Resultado de as_retriever {doc.page_content}')
        print()