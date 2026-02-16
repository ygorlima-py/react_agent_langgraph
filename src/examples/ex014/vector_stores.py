from langchain_core.vectorstores import InMemoryVectorStore
from examples.ex014.utils import embeddings_model
from examples.ex014.pdf_loader import load_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich import print

documents = load_documents()

'''
InMemoryVectorStore é um banco de dados na memória que salva vetores
A partir dele você pode instânciar e manipula-lo adicionando
documentos com add_docuemnts(), deletar documentos com delete()
'''
vector_store = InMemoryVectorStore(embedding=embeddings_model())

''' 
O ideal é fazer chunking com RecursiveCharacterTextSplitter
dos docuemntos e passar as o chunkings para add_docuemnts
'''
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(documents=documents)

'''
Aqui em add_documents vamos passar uma lista de chunks, que são
docuementos ja quebrados pelo text splits. Assim fica mais
fácil ao fazermos as buscas. add_documents salva na memória
os vetores juntamente com os trechos de textos. Neste caso
estamos trabalhando com a memória ram pois vectore_store é 
uma instância de InMemoryVectorStore. Quando tivermos em produção
o ideal é salvar no banco de dados. Por exemplo PGVector que 
trabalha com Postgre. Ou ainda Chroma para armazenar vetores locais

'''
vector_store.add_documents(documents=all_splits)

'''
Aqui nós realizaremos a busca por similariedade, como?
aqui iremos passar o que queremos buscar no documento
como argumento de similarity_search(), que irá retornar
uma lista de documentos com conteudos que mais
se aproximam da minha busca

os parâmetros mais usados em similarty_search
- query = texto de busca em str (obrigatório)

- k= os trechos mais próximos, nesse caso ele trouxe
os 3 trchos mais próximos

- filter= um dict com as chves do metadata para ajudar na busca do
docuemento. Neste caso filter está dando errado quando
uso InMemoryVectorStore, pois quando uso dict aparece o erro de
TypeError informando que o filter só aceita objetos callable
que são chamados
'''
similar_docs = vector_store.similarity_search(
    query="Lucro do periodo?",
    k=3,
    # filter=lambda doc: doc.metadata.get("source") == "resultado_bbas3_4t_2025",
    )

print(similar_docs)

