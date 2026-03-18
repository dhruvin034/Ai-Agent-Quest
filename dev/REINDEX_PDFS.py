#!/usr/bin/env python3
"""
Force re-index PDFs into vector database
Run this if documents are not being found
"""

import os
import sys
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

print("\n" + "="*60)
print("🔄 RE-INDEXING PDFs")
print("="*60 + "\n")

# Path setup
vector_db_path = os.path.join(os.path.dirname(__file__), "vector_storage")
data_path = os.path.join(os.path.dirname(__file__), "data")

# Step 1: Delete existing vector DB
print("🗑️  Deleting old vector database...")
if os.path.exists(vector_db_path):
    shutil.rmtree(vector_db_path)
    print(f"   ✅ Deleted: {vector_db_path}")
else:
    print("   ℹ️  Vector DB didn't exist")

# Step 2: Check PDFs exist
print("\n📄 Checking PDFs...")
if os.path.exists(data_path):
    pdf_files = [f for f in os.listdir(data_path) if f.endswith(".pdf")]
    if pdf_files:
        print(f"   ✅ Found {len(pdf_files)} PDFs:")
        for pdf in pdf_files:
            print(f"      - {pdf}")
    else:
        print(f"   ❌ No PDF files in {data_path}")
        sys.exit(1)
else:
    print(f"   ❌ Data folder not found at {data_path}")
    sys.exit(1)

# Step 3: Re-index
print("\n⚙️  Re-indexing documents...")
try:
    from app.ingest.pdf_ingest import ingest_documents
    ingest_documents()
    print("\n   ✅ Re-indexing complete!")
    
except Exception as e:
    print(f"\n   ❌ Error during re-indexing: {e}")
    sys.exit(1)

# Step 4: Verify
print("\n✔️  Verifying vector database...")
try:
    from app.config.embeddings import get_embeddings
    from langchain_chroma import Chroma
    
    embeddings = get_embeddings()
    vectordb = Chroma(
        persist_directory=vector_db_path,
        embedding_function=embeddings
    )
    
    doc_count = vectordb._collection.count()
    print(f"   ✅ Vector DB now contains {doc_count} document chunks")
    
    if doc_count == 0:
        print("   ⚠️  Vector DB is empty - there may be an issue with the PDFs")
    
except Exception as e:
    print(f"   ⚠️  Error verifying: {e}")

print("\n" + "="*60)
print("✅ Done! Now try: python app/main.py")
print("="*60 + "\n")
