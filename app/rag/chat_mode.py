from config.llm import get_llm
from memory.chat_memory import load_memory, add_to_memory

llm = get_llm()

def chat_response(question):

    history = load_memory()

    history_text = ""

    for item in history[-5:]:
        history_text += f"User: {item['question']}\nAssistant: {item['answer']}\n"

    prompt = f"""
You are a helpful assistant.

Conversation history:
{history_text}

User:
{question}

Respond naturally.
"""

    response = llm.invoke(prompt)

    answer = response.content

    add_to_memory(question, answer)

    return answer