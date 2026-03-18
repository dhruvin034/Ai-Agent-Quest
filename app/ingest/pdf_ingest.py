import os
import sys

# Add parent directory to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from config.embeddings import get_embeddings
from ingest.upload_handler import add_document_metadata, update_document_chunks, ensure_directories

# Fix Windows paths
VECTOR_DB = os.path.join(os.path.dirname(__file__), "..", "..", "vector_storage")
VECTOR_DB = os.path.abspath(VECTOR_DB)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data")
DATA_PATH = os.path.abspath(DATA_PATH)


def ingest_documents(reset: bool = True):
    """
    Ingest all PDF documents from data folder
    
    Args:
        reset: If True, create new vector DB (overwrite). If False, add to existing.
    """
    ensure_directories()
    
    documents = []

    for file in os.listdir(DATA_PATH):

        if file.endswith(".pdf"):

            path = os.path.join(DATA_PATH, file)
            print("Loading:", path)

            loader = PyPDFLoader(path)

            docs = loader.load()

            documents.extend(docs)
            print(f"  ✓ Loaded {len(docs)} pages")

    print(f"\n📝 Total pages loaded: {len(documents)}")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)
    print(f"🔪 Split into {len(chunks)} chunks")

    embeddings = get_embeddings()

    print("🧠 Creating embeddings and storing in vector DB...")
    
    if reset and os.path.exists(VECTOR_DB):
        # Remove old vector DB to start fresh
        import shutil
        shutil.rmtree(VECTOR_DB)
        vectordb = Chroma.from_documents(
            chunks,
            embedding=embeddings,
            persist_directory=VECTOR_DB
        )
    else:
        # Create new or add to existing
        if os.path.exists(VECTOR_DB):
            vectordb = Chroma(
                persist_directory=VECTOR_DB,
                embedding_function=embeddings
            )
            vectordb.add_documents(chunks)
        else:
            vectordb = Chroma.from_documents(
                chunks,
                embedding=embeddings,
                persist_directory=VECTOR_DB
            )

    # Track documents in metadata
    pdf_files = [f for f in os.listdir(DATA_PATH) if f.endswith(".pdf")]
    for pdf_file in pdf_files:
        add_document_metadata(pdf_file, pdf_file, "indexed")
    
    print(f"\n✅ Success! Ingested {len(chunks)} document chunks")
    print(f"📍 Stored at: {VECTOR_DB}")


if __name__ == "__main__":
    try:
        ingest_documents()
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()