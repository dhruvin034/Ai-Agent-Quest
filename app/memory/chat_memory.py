import json
import os

MEMORY_FILE = "chat_memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def add_to_memory(question, answer):

    memory = load_memory()

    memory.append({
        "question": question,
        "answer": answer
    })

    save_memory(memory)