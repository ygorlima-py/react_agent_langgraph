from examples.ex015.load_vector_stores import load_vector_stores
from examples.ex015.utils import load_llm
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.retrieval import create_retrieval_chain
from rich import print, markdown

# Carrega o Vectore Store
vector_store = load_vector_stores()

'''
as_retriever é um método do Chroma o db vector que retorna 
um VectorStoreRetriever, este objeto possui métodos como
o invoke que será falado abaixo. Os argumentos são:

- search_type: A forma matemática de selecionar os trechos mais próximos, 
aqui usamos MMR (Maximal Marginal Relevance). Exemplo, se fectch_k=15 ele busca
os 15 documentos mais próximo da pergunta, e se k = 4, ele filtra
os 4 documentos mais próximos da pergunta dentro dos 15.

'''

retriever = vector_store.as_retriever(
    search_type="mmr", search_kwargs={"k": 4, "fetch_k": 15, "lambda_mult": 0.35}
)

llm = load_llm()

system_prompt = (
 """
  You are a helpful, precise assistant. Follow these rules:

     Always answer using only the information provided in the CONTEXT.
     If the CONTEXT does not contain enough information to answer, say: “I don’t have enough information in the provided context to answer that.”
     Do not guess, invent facts, or use outside knowledge.
     When the user asks for a step-by-step solution, provide clear steps, but keep them concise.
     If the user’ s request is ambiguous, ask a single clarifying question before answering.
     Keep the tone professional and direct.
    
    CONTEXT
    {context}
 """
)

prompt = ChatPromptTemplate.from_messages(   
   [
       ("system", system_prompt),
       ("human", "{input}")
   ]
)

''' A qui'''
question_answer_chain = create_stuff_documents_chain(llm, prompt)

retrieval_chain = create_retrieval_chain(retriever, question_answer_chain)

while True:
    ask = input("Humano: ")
    
    if ask in ['exist', 'q', 'sair']:
        break
    response = retrieval_chain.invoke({"input":"Olá LLM, análise o lucro do bbsa3 no ultimo trimestre"})
    
    print(markdown.Markdown("--------------------------------------"))
    
    print(response["answer"])


