from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from examples.ex014.env import get_env
from langchain_community.retrievers import KNNRetriever
from rich import print


""" 
Extraindo os dados do pdf com os PdfLoaders do LangChain
Aqui load() retorna uma lista de docuemntos

"""
file_path = "src/examples/ex013/ex013_data/resultado_bbas3_4t_2025.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()
# print(f"{docs[0].page_content[:700]}\n")
# print(docs[0].metadata)

# ----------------------------- Chunk --------------------------------

""" 
Aqui, usaremos um divisor de texto simples 
que divide o texto com base em caracteres. Dividiremos nossos 
documentos em blocos de 1000 caracteres com 200 caracteres de
sobreposição entre os blocos.

O RecursiveCharacterTextSplitter tenta respeitar
separadores, paragrafos, espaços linhas podem 
variar 950, 970, 980... caracteres

Conforme o exemplo abaixo com chunk_overlap com 200,
significa que o texto avana na faixa de 800 caracteres

chunk_size : Quantidade de caracteres por parte
chunk_overlap: é a sobreposição dos caracteres

"""
# Crio uma instância de RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)

all_splits = text_splitter.split_documents(docs)

# print(all_splits[0])


#----------------------------Embendings--------------------------------

"""
- Aqui pegamos os chunks que são pedaços de texto com o tamanho
de até 1000 caracteres conforme configuramos no chunk_size

- Fazemos uma list comprehension extraindo o conteudo
de cada split

- Injetamos a lista com os conteúdos em embed_documents
retornando uma lista de float com cada embend

"""
OPENROUTER_API_KEY: str = get_env("OPENROUTER_API_KEY")

embeddings = OpenAIEmbeddings(
    model="sentence-transformers/all-minilm-l6-v2",
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    tiktoken_enabled=False,
)

documents = [split.page_content for split in all_splits]

# documents_embds = embeddings.embed_documents(documents)

# print(len(documents_embds))


""" 
Aqui iremos embedar a nossa consulta, ou seja
transformar em embedding
"""
query = "Qual foi o lucro do banco no 4 trimestre de 2025?"
query_embd = embeddings.embed_query(query)


""" 
O KNNRetriever faz todas as operações citadas acima

- from_text aceita uma lista de string como documentos e a embendings, que é o
modelo que vai realizar a operação de transformação do texto da docs e da query
em embendings.

-Ao final ele faz a busca no pdf dos rechos que mais se relaciona
com a query. Isso é feito com similaridade de cosseno
"""
retriever = KNNRetriever.from_texts(documents, embeddings)
result = retriever.invoke(query)


print(result)