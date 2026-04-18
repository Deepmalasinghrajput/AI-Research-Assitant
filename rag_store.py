from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

# persistent DB (IMPORTANT)
vector_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

def add_to_db(text: str, meta: dict = None):
    chunks = splitter.split_text(text)

    vector_db.add_texts(
        texts=chunks,
        metadatas=[meta or {} for _ in chunks]
    )

    vector_db.persist()



def search_db(query: str, k=4):
    docs = vector_db.similarity_search(query, k=k)
    return "\n\n".join([d.page_content for d in docs])