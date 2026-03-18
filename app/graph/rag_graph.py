from langgraph.graph import StateGraph, END
from typing import TypedDict

from agent.planner import decide_tool
from tools.rag_tool import rag_tool
from tools.chat_tool import chat_tool
from rag.retriever import get_retriever
from rag.generator import generate_answer
from rag.verifier import verify_answer


class AgentState(TypedDict):

    question: str
    route: str
    answer: str
    sources: list


def planner_node(state):

    question = state["question"]

    route = decide_tool(question)

    print("\n🧠 Agent Decision:")
    print(f"Selected Tool → {route.upper()}")

    return {"route": route}


def rag_node(state):

    result = rag_tool(state["question"])

    # If RAG failed to find docs, fall back to chat mode
    if not result.get("sources") and "No relevant document" in result.get("answer", ""):
        answer = chat_tool(state["question"])
        return {"answer": answer, "sources": []}

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }


def chat_node(state):

    answer = chat_tool(state["question"])

    return {
        "answer": answer,
        "sources": []
    }

# GENERATE NODE  ← ADD YOUR CODE HERE
def generate_node(state):

    docs = state["documents"]

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    answer, sources = generate_answer(
        context,
        state["question"],
        docs
    )

    verified = verify_answer(
        context,
        state["question"],
        answer
    )

    if not verified:
        answer = "I could not verify the answer from the document."

    return {
        "answer": answer,
        "sources": sources
    }

builder = StateGraph(AgentState)

builder.add_node("planner", planner_node)
builder.add_node("rag", rag_node)
builder.add_node("chat", chat_node)

builder.set_entry_point("planner")

builder.add_conditional_edges(
    "planner",
    lambda x: x["route"],
    {
        "rag": "rag",
        "chat": "chat"
    }
)

builder.add_edge("rag", END)
builder.add_edge("chat", END)

rag_graph = builder.compile()