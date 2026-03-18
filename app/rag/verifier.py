from config.llm import get_llm

llm = get_llm()


def verify_answer(context, question, answer):

    prompt = f"""
Verify if the answer is supported by the context.

Context:
{context}

Question:
{question}

Answer:
{answer}

Respond with:

SUPPORTED
or
NOT_SUPPORTED
"""

    response = llm.invoke(prompt)

    label = response.content.strip().upper()

    return "SUPPORTED" in label