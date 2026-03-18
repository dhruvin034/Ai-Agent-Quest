from config.llm import get_llm
from memory.chat_memory import add_to_memory

llm = get_llm()


def generate_answer(context, question, documents):

    citations = []

    for doc in documents:

        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", None)

        if page is not None:
            citations.append(f"{source} (page {page+1})")
        else:
            citations.append(source)

    prompt = f"""
Answer the question using the context.

Context:
{context}

Question:
{question}

Answer clearly and reference the document.
"""

    response = llm.invoke(prompt)

    answer = response.content

    # store memory
    add_to_memory(question, answer)

    return answer, list(set(citations))