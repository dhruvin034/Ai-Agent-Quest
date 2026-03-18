from config.llm import get_llm
from memory.chat_memory import load_memory, add_to_memory

llm = get_llm()


def chat_tool(question):

    history = load_memory()

    history_text = ""

    for item in history[-5:]:
        history_text += f"User: {item['question']}\nAssistant: {item['answer']}\n"

    prompt = f"""You are a helpful, conversational assistant. Remember user information from conversation.

IMPORTANT: 
- If user asks about themselves (my name, who am I, etc), use conversation history to answer
- If they said "my name is X", remember that and refer to them as X
- Answer conversational questions using context from chat history
- Be friendly and personal

Conversation history (recent messages):
{history_text}

User question:
{question}

Respond naturally and use information from the conversation history to personalize your response."""

    response = llm.invoke(prompt)

    answer = response.content

    add_to_memory(question, answer)

    return answer