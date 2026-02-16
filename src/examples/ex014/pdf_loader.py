from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def load_documents() -> list[Document]:
    file_path = "src/examples/ex013/ex013_data/resultado_bbas3_4t_2025.pdf"
    loader = PyPDFLoader(file_path)
    return loader.load()