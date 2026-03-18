"""
📤 Upload Handler Module
Handles dynamic file uploads and ingestion with metadata tracking
"""

import os
import sys
import json
import tempfile
from datetime import datetime
from typing import List, Dict, Tuple

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from config.embeddings import get_embeddings

# Fix Windows paths
VECTOR_DB = os.path.join(os.path.dirname(__file__), "..", "..", "vector_storage")
VECTOR_DB = os.path.abspath(VECTOR_DB)

METADATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "document_metadata.json")
METADATA_PATH = os.path.abspath(METADATA_PATH)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
UPLOAD_FOLDER = os.path.abspath(UPLOAD_FOLDER)


def ensure_directories():
    """Create necessary directories if they don't exist"""
    os.makedirs(VECTOR_DB, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def load_metadata() -> Dict:
    """Load document metadata from JSON file"""
    if os.path.exists(METADATA_PATH):
        try:
            with open(METADATA_PATH, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading metadata: {e}")
            return {"documents": []}
    return {"documents": []}


def save_metadata(metadata: Dict):
    """Save document metadata to JSON file"""
    try:
        with open(METADATA_PATH, 'w') as f:
            json.dump(metadata, f, indent=2)
    except Exception as e:
        print(f"❌ Error saving metadata: {e}")


def add_document_metadata(filename: str, original_name: str, status: str = "indexed") -> Dict:
    """Add document metadata entry"""
    metadata = load_metadata()
    
    doc_entry = {
        "id": len(metadata["documents"]) + 1,
        "filename": filename,
        "original_name": original_name,
        "upload_date": datetime.now().isoformat(),
        "status": status,
        "chunks": 0
    }
    
    metadata["documents"].append(doc_entry)
    save_metadata(metadata)
    
    return doc_entry


def update_document_chunks(original_name: str, chunk_count: int):
    """Update chunk count for a document"""
    metadata = load_metadata()
    
    for doc in metadata["documents"]:
        if doc["original_name"] == original_name:
            doc["chunks"] = chunk_count
            save_metadata(metadata)
            break


def ingest_single_document(file_path: str, file_name: str) -> Tuple[bool, str, int]:
    """
    Ingest a single PDF document and add to existing vector DB
    
    Args:
        file_path: Path to the PDF file
        file_name: Original name of the file
        
    Returns:
        Tuple[success: bool, message: str, chunk_count: int]
    """
    try:
        ensure_directories()
        
        print(f"\n📥 Processing: {file_name}")
        
        # Load PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        if not docs:
            return False, f"Failed to load PDF: {file_name}", 0
        
        print(f"   ✓ Loaded {len(docs)} pages")
        
        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )
        chunks = splitter.split_documents(docs)
        print(f"   ✓ Split into {len(chunks)} chunks")
        
        # Get embeddings
        embeddings = get_embeddings()
        
        # Add to vector DB (or create if doesn't exist)
        if os.path.exists(VECTOR_DB):
            # Add to existing DB
            vectordb = Chroma(
                persist_directory=VECTOR_DB,
                embedding_function=embeddings
            )
            vectordb.add_documents(chunks)
            print(f"   ✓ Added to existing vector DB")
        else:
            # Create new DB
            vectordb = Chroma.from_documents(
                chunks,
                embedding=embeddings,
                persist_directory=VECTOR_DB
            )
            print(f"   ✓ Created new vector DB")
        
        # Save metadata
        add_document_metadata(file_name, file_name, "indexed")
        update_document_chunks(file_name, len(chunks))
        
        message = f"✅ Successfully ingested '{file_name}': {len(chunks)} chunks added"
        print(f"   {message}\n")
        
        return True, message, len(chunks)
        
    except Exception as e:
        error_msg = f"❌ Error ingesting {file_name}: {str(e)}"
        print(f"   {error_msg}\n")
        return False, error_msg, 0


def ingest_uploaded_files(uploaded_files) -> Dict:
    """
    Process multiple uploaded files
    
    Args:
        uploaded_files: List of uploaded file objects (from Streamlit)
        
    Returns:
        Dict with processing results
    """
    results = {
        "total": len(uploaded_files),
        "successful": 0,
        "failed": 0,
        "total_chunks": 0,
        "messages": [],
        "errors": []
    }
    
    for uploaded_file in uploaded_files:
        # Save uploaded file to temp location
        temp_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        
        try:
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process file
            success, message, chunks = ingest_single_document(
                temp_path, 
                uploaded_file.name
            )
            
            if success:
                results["successful"] += 1
                results["total_chunks"] += chunks
                results["messages"].append(message)
            else:
                results["failed"] += 1
                results["errors"].append(message)
                
        except Exception as e:
            error_msg = f"Failed to save uploaded file: {str(e)}"
            results["failed"] += 1
            results["errors"].append(error_msg)
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
    
    return results


def get_indexed_documents() -> List[Dict]:
    """Get list of all indexed documents"""
    metadata = load_metadata()
    return metadata.get("documents", [])


def delete_document(doc_name: str) -> Tuple[bool, str]:
    """Delete a document from vector DB and metadata"""
    try:
        metadata = load_metadata()
        
        # Remove from metadata
        metadata["documents"] = [
            doc for doc in metadata["documents"] 
            if doc["original_name"] != doc_name
        ]
        save_metadata(metadata)
        
        # Note: Chroma doesn't have built-in delete by document name
        # For production, consider implementing selective deletion
        # or use a different approach (e.g., filter by metadata)
        
        return True, f"Document '{doc_name}' removed from tracking"
        
    except Exception as e:
        return False, f"Error deleting document: {str(e)}"


def get_vector_db_stats() -> Dict:
    """Get statistics about the vector database"""
    try:
        if not os.path.exists(VECTOR_DB):
            return {
                "exists": False,
                "document_count": 0,
                "chunk_count": 0,
                "status": "Vector DB not initialized"
            }
        
        embeddings = get_embeddings()
        vectordb = Chroma(
            persist_directory=VECTOR_DB,
            embedding_function=embeddings
        )
        
        chunk_count = vectordb._collection.count()
        
        return {
            "exists": True,
            "document_count": len(get_indexed_documents()),
            "chunk_count": chunk_count,
            "status": "Ready" if chunk_count > 0 else "Empty",
            "location": VECTOR_DB
        }
        
    except Exception as e:
        return {
            "exists": False,
            "document_count": 0,
            "chunk_count": 0,
            "status": f"Error: {str(e)}"
        }


def reset_vector_db() -> Tuple[bool, str]:
    """Reset the vector database and metadata"""
    try:
        import shutil
        
        if os.path.exists(VECTOR_DB):
            shutil.rmtree(VECTOR_DB)
            
        metadata = {"documents": []}
        save_metadata(metadata)
        
        return True, "Vector database reset successfully"
        
    except Exception as e:
        return False, f"Error resetting vector DB: {str(e)}"


if __name__ == "__main__":
    # Test the module
    stats = get_vector_db_stats()
    print("\n📊 Vector DB Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
