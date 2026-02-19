from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from rich import print

def load_documents() -> list[Document]:
    files = [
        "anomalia_soja",
        "anomaliaemsoja",
    ]
    
    list_docs = []
    for file in files:
        file_path = f"src/examples/ex016/ex016_data/{file}.pdf"
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        for doc in docs:
            list_docs.append(doc)
            
    return list_docs


if __name__ == "__main__":
    response = load_documents()
    print(response)