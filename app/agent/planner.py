from rag.query_router import classify_query


def decide_tool(question):
    """Route question to RAG or chat using classifier."""

    label = classify_query(question)

    if label == "document":
        return "rag"

    return "chat"