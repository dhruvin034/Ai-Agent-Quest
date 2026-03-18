from config.llm import get_llm
from memory.chat_memory import load_memory

llm = get_llm()


def rewrite_query(query):

    history = load_memory()

    history_text = ""

    for item in history[-5:]:
        history_text += f"User: {item['question']}\nAssistant: {item['answer']}\n"

    prompt = f"""
You improve questions for document search.

Conversation history:
{history_text}

User question:
{query}

Rewrite the question so it includes missing context.
Return only the improved query.
"""

    response = llm.invoke(prompt)

    return response.content.strip()