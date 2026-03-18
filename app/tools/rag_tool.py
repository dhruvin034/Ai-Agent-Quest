from rag.retriever import get_retriever
from rag.generator import generate_answer
from rag.query_router import classify_query
from rag.query_rewriter import rewrite_query
from rag.hybrid_retriever import hybrid_retrieve
from rag.verifier import verify_answer


def _fetch_documents(retriever, query):
    if hasattr(retriever, "get_relevant_documents"):
        return retriever.get_relevant_documents(query)
    if hasattr(retriever, "retrieve"):
        return retriever.retrieve(query)
    if hasattr(retriever, "invoke"):
        return retriever.invoke(query)
    raise AttributeError("Retriever has no supported fetch method")


def rag_tool(question):
    # Note: Already routed to RAG by planner, no need to re-check classification
    
    print("\n🔍 RAG Pipeline:")
    
    # Step 1: Rewrite query
    rewritten_query = rewrite_query(question)
    search_query = rewritten_query if rewritten_query else question
    print(f"   📝 Query rewritten: {search_query[:70]}...")

    # Step 2: Retrieve documents
    retriever = get_retriever()
    docs = _fetch_documents(retriever, search_query) or []
    print(f"   📚 Documents found: {len(docs)}")

    if not docs:
        print(f"\n   ⚠️  ERROR: No documents retrieved!")
        print("   Make sure:")
        print("   1. PDFs exist in data/ folder")
        print("   2. Run indexing: from ingest.pdf_ingest import ingest_documents; ingest_documents()")
        print("   3. Delete vector_storage/ folder if documents changed\n")
        return {
            "answer": "No relevant document chunks were found for this query.",
            "sources": []
        }

    # Step 3: Hybrid retrieval
    docs = hybrid_retrieve(search_query, docs)
    print(f"   🔗 After hybrid retrieval: {len(docs)} results")

    # Step 4: Generate answer
    context = "\n\n".join([doc.page_content for doc in docs])
    answer, sources = generate_answer(context, question, docs)
    print(f"   ✅ Answer generated")

    # Step 5: Verify answer
    if not verify_answer(context, question, answer):
        answer = "I could not verify the answer from the document."
        print(f"   ⚠️  Verification failed\n")
    else:
        print(f"   ✅ Verified\n")

    return {
        "answer": answer,
        "sources": sources
    }