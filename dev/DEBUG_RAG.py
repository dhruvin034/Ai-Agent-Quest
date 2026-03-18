#!/usr/bin/env python3
"""
Debug script to diagnose RAG pipeline issues
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

print("\n" + "="*60)
print("🔧 RAG PIPELINE DIAGNOSTIC")
print("="*60 + "\n")

# 1. Check if data files exist
print("📂 Checking data files...")
data_path = os.path.join(os.path.dirname(__file__), "data")
if os.path.exists(data_path):
    pdf_files = [f for f in os.listdir(data_path) if f.endswith(".pdf")]
    print(f"   ✅ Data folder found at: {data_path}")
    print(f"   📄 PDFs found: {len(pdf_files)}")
    for pdf in pdf_files:
        print(f"      - {pdf}")
else:
    print(f"   ❌ Data folder not found at: {data_path}")

# 2. Check if vector DB exists
print("\n💾 Checking vector database...")
vector_db_path = os.path.join(os.path.dirname(__file__), "vector_storage")
if os.path.exists(vector_db_path):
    print(f"   ✅ Vector DB folder found at: {vector_db_path}")
    db_files = os.listdir(vector_db_path)
    print(f"   📋 Files in vector_storage: {len(db_files)}")
    for f in db_files[:10]:  # Show first 10
        print(f"      - {f}")
else:
    print(f"   ❌ Vector DB not found at: {vector_db_path}")
    print("   💡 Run: python app/ingest/pdf_ingest.py")

# 3. Check vector DB contents
print("\n🔍 Checking vector DB contents...")
try:
    from app.rag.retriever import get_retriever
    from langchain_chroma import Chroma
    from app.config.embeddings import get_embeddings
    
    embeddings = get_embeddings()
    vectordb = Chroma(
        persist_directory=vector_db_path,
        embedding_function=embeddings
    )
    
    doc_count = vectordb._collection.count()
    print(f"   📊 Documents in vector DB: {doc_count}")
    
    if doc_count > 0:
        print("   ✅ Vector DB has documents!")
        
        # Test retrieval
        print("\n🧪 Testing retrieval...")
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})
        
        test_query = "invoice number"
        docs = retriever.invoke(test_query)
        print(f"   Query: '{test_query}'")
        print(f"   Results: {len(docs)} documents")
        
        if len(docs) > 0:
            print("   📄 Top result:")
            print(f"      {docs[0].page_content[:150]}...")
            print(f"      Source: {docs[0].metadata.get('source', 'unknown')}")
        else:
            print("   ⚠️  No results found - query may not match documents")
    else:
        print("   ❌ Vector DB is EMPTY!")
        print("   💡 Run: python app/ingest/pdf_ingest.py")
        
except Exception as e:
    print(f"   ❌ Error checking vector DB: {e}")
    print(f"   Type: {type(e).__name__}")

# 4. Test LLM connection
print("\n🤖 Checking LLM connection...")
try:
    from app.config.llm import get_llm
    llm = get_llm()
    
    # Try a simple query
    response = llm.invoke("Say 'working' in one word")
    if response and response.content:
        print(f"   ✅ LLM working: {response.content.strip()}")
    else:
        print(f"   ❌ LLM returned empty response")
        
except Exception as e:
    print(f"   ❌ LLM error: {e}")
    print(f"   Make sure OPENROUTER_API_KEY is set in .env file")

# 5. Test query classification
print("\n🧠 Testing query classification...")
try:
    from app.rag.query_router import classify_query
    
    test_queries = [
        "What is the invoice number?",
        "How are you?",
        "Find the total amount"
    ]
    
    for q in test_queries:
        result = classify_query(q)
        print(f"   '{q}'")
        print(f"      → {result.upper()}")
        
except Exception as e:
    print(f"   ❌ Classification error: {e}")

print("\n" + "="*60)
print("✅ Diagnostic complete!")
print("="*60 + "\n")

# Recommendations
print("🎯 NEXT STEPS:\n")
if not os.path.exists(vector_db_path):
    print("1. ⚠️  Vector DB missing - Run this to index PDFs:")
    print("   cd app")
    print("   python -c \"from ingest.pdf_ingest import ingest_documents; ingest_documents()\"")
    print("")

print("2. To test the full RAG pipeline:")
print("   cd app")
print("   python main.py")
print("")

print("3. Try asking:")
print("   - 'What is the invoice number?'")
print("   - 'Who is the client?'")
print("   - 'What is the total amount?'")
print("")
