from rag.retriever import get_retriever


try:
    from rank_bm25 import BM25Okapi
    _HAS_BM25 = True
except ImportError:
    BM25Okapi = None
    _HAS_BM25 = False


def hybrid_retrieve(question, documents):

    # Vector retrieval
    retriever = get_retriever()
    vector_docs = retriever.invoke(question)

    if not _HAS_BM25 or not documents:
        return vector_docs

    # BM25 keyword retrieval
    corpus = [doc.page_content for doc in documents]
    tokenized = [doc.split() for doc in corpus]
    bm25 = BM25Okapi(tokenized)

    scores = bm25.get_scores(question.split())
    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    keyword_docs = [x[0] for x in ranked[:3]]

    # merge results
    results = vector_docs + keyword_docs

    # remove duplicates, preserve order
    unique = []
    seen = set()

    for doc in results:
        key = doc.page_content
        if key not in seen:
            unique.append(doc)
            seen.add(key)

    return unique