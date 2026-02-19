from langchain_community.retrievers import BM25Retriever
from examples.ex016.text_splitter import splitter_documents
from examples.ex016.pdf_loader import load_documents
from langchain_core.documents import Document
from rich import print

'''
Aqui iremos pegar o texto dos documentos para realizarmos BM25
neste exemplos podemos buscar os docuemntos de 3 formas
1 - Como temos o pdf, podemos acessar o pds, fazer chunk
e pegar o texto e passar como argumento. É o que vamos fazer 
nesse exemplo

2- Caso não tenhamos os pdf no projeto (mais comum em produção)
pegamos os documentos em texto do vectore store, na qual é guardado
emedings, texto e metadados

3 - A terceira opção é mais porfissional, armazenamos os textos
e metadata em um Postgre e realizamos a pesquisade lá, más usado 
em projetos escaláveis
'''

def search_bm_25_retriever(documents: list[Document]) -> BM25Retriever:
    '''
    BM 25 É um algorítimo que faz buscas por match de palavras com base em textos.
    diferentemente de outros retrievers como o as_retriever e o 
    ContextualCompressionRetriever que fazem busca vetorial ou
    seja pegam os vetores mais próximos aos vetores das queries, o 
    BM 25 faz a busca através de palavras chaves. No exemplo
    estamos usando um documento com que fala a respeito da anomalia
    da soja, neste docuemnto usamos a query olimpo, em BM 25 tivemos
    como retorno dos splts que continham a palavra chave olimpo. 
    Muito bom para trechos curtos e tabelas. 
    
    A seguir unimos o resultado de as_retriever e BM_25 e rerankiamos e aplicamos
    no pront para dar a resposta. Usamos isso com EnsembleRetriever
    '''
    
    splits = splitter_documents(documents=documents)

    bm_25_retriever = BM25Retriever.from_documents(
        documents=splits,
    )
    
    # Numero de documentos que vão retornar
    bm_25_retriever.k = 50
    
    return bm_25_retriever

if __name__ == "__main__":
    
    documents = load_documents()
    bm_25_retriever = search_bm_25_retriever(documents=documents)
    docs_retriever_bm25 = bm_25_retriever.invoke('Olimpo')
    
    for doc in docs_retriever_bm25:
        print('--------------------------------')
        print(f'Resultado Algoritimo BM25: {doc.page_content}')