from examples.ex014.utils import embeddings_model
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from examples.ex014.pdf_loader import load_documents
from rich import print

documents = load_documents()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)

# Quebrando o docuemnto em pedaços
all_splits = text_splitter.split_documents(documents=documents)

# Gerando id para cada documento usando informações de metadata
ids = [f"{split.metadata['page_label']}:{split.metadata['start_index']}:{split.metadata['source']}" for split in all_splits]

'''
Aqui criamos uma instância do Banco de vetores Chroma
collection_name = nome do banco de dados,
embedding_function = o modelo carregado,
persist_directory = nome da pasta onde os dados vão ficar salvos
'''
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings_model(),
    persist_directory="./chroma_langchain_db",
)

''' Adicionando os documentos e os ids de cada um no Chroma'''
# vector_store.add_documents(documents=all_splits, ids=ids)

'''Fazendo a busca simples por similaridade'''
# results = vector_store.similarity_search(
#     'Qual foi o endividamento da empresa?', 
#     k=2, 
# )

# for res in results:
#     print(f'* {res.page_content} [{res.metadata}]')


''' Busca por similaridade com pontuação
- Aqui execultamos uma busca por similaridade recebendo
as respectivas pontuações de cada trecho de texto.
'''
results = vector_store.similarity_search_with_score(
    'Como foin o lucro líquido ajustado?', 
    k=3, 
)


for res, score in results:
    print(f"* [SIM={score:3f}] {res.page_content} [{res.metadata}]")
