from langchain_chroma import Chroma
from config.embeddings import get_embeddings
import os

# Fix Windows path
VECTOR_DB = os.path.join(os.path.dirname(__file__), "..", "..", "vector_storage")
VECTOR_DB = os.path.abspath(VECTOR_DB)

embeddings = get_embeddings()

vectordb = Chroma(
    persist_directory=VECTOR_DB,
    embedding_function=embeddings
)

retriever = vectordb.as_retriever(search_kwargs={"k": 5})


def get_retriever():
    # Verify vector DB has documents before returning
    try:
        doc_count = vectordb._collection.count()
        if doc_count == 0:
            print("⚠️  WARNING: Vector DB is EMPTY")
            print(f"   Location: {VECTOR_DB}")
            print("   Please run: python ingest/pdf_ingest.py")
        else:
            print(f"✅ Vector DB loaded: {doc_count} chunks")
    except Exception as e:
        print(f"⚠️  Error checking vector DB: {e}")
    
    return retriever