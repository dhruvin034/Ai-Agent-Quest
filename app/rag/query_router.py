from config.llm import get_llm
import re

llm = get_llm()

def classify_query(question):
    """
    Classify whether question is about document content (DOCUMENT) 
    or general conversation (CHAT).
    
    Key distinction:
    - DOCUMENT: Extract/find information FROM documents (invoice number, job title, etc)
    - CHAT: Conversation, user state, memory, general knowledge (my name, how are you, etc)
    """
    
    # Conversational/Memory keywords - HIGH PRIORITY (check first!)
    chat_keywords = [
        # Greetings
        "hello", "hi", "hey", "goodbye", "bye", "thanks", "thank you",
        # User state questions
        "my name", "i am", "i'm", "my ", "remember me", "do you remember",
        "who am i", "tell me about me", "about myself", "my personal",
        # Conversational
        "how are you", "how do you feel", "what do you think", "tell me a joke",
        "general knowledge", "what time", "what's the weather", "current date",
        # Negations of document queries
        "don't know", "no document", "not in", "outside", "beyond"
    ]
    
    # Document extraction keywords
    document_keywords = [
        "invoice", "document", "file", "page", "section", "chapter",
        "find in", "extract from", "look up in", "search the",
        "from the document", "in the file", "according to",
        "locate", "retrieve", "pull", "get the", "what's the",
        "total", "amount", "number", "cost", "price", "date", "title",
        "client", "customer", "company", "organization", "position",
        "requirements", "skills", "responsibilities"
    ]
    
    question_lower = question.lower().strip()
    
    # Check CHAT keywords FIRST (high priority) - these override everything
    for keyword in chat_keywords:
        if keyword in question_lower:
            # Avoid false negatives - "what is the title" should still be document
            if not any(doc_kw in question_lower for doc_kw in ["title job", "title of the job", "position", "role"]):
                return "chat"
    
    # Check if it's asking for user's personal information
    if re.search(r"\b(my|tell me about myself|do you remember me|who am i)\b", question_lower):
        return "chat"
    
    # Check document keywords
    for keyword in document_keywords:
        if keyword in question_lower:
            # Exclude conversational context
            if "my " not in question_lower or keyword in ["total", "amount", "number", "cost", "price"]:
                return "document"
    
    # Check if asking about user's information
    if "name" in question_lower and "my" in question_lower:
        return "chat"
    
    # If no keywords match, use LLM as fallback with strong context
    prompt = f"""You are a strict question classifier for a Document RAG system.

DOCUMENT questions = Extract/lookup information FROM documents
- "What invoice number is in the document?" → DOCUMENT
- "Extract the job title" → DOCUMENT
- "Find the total amount" → DOCUMENT
- "What company is mentioned?" → DOCUMENT

CHAT questions = Conversational/personal/memory questions NOT requiring document lookup
- "What is my name?" → CHAT (asking about user's personal data, NOT in documents)
- "Can you remember me?" → CHAT (conversational memory)
- "How are you?" → CHAT (greeting)
- "Who am I?" → CHAT (about user's identity, not document)
- "Tell me about myself" → CHAT (personal information)

CRITICAL: If question asks about USER'S NAME, IDENTITY, or MEMORY → Always CHAT
Even if "name" appears, context matters. "My name", "who am I" = CHAT, not document lookup.

User question: {question}

Respond with ONE WORD ONLY: DOCUMENT or CHAT

Think carefully about whether this requires document lookup or is about user conversation."""

    response = llm.invoke(prompt)
    label = response.content.strip().upper()
    
    # Log for debugging
    print(f"   🧠 Router: '{question[:50]}...' → {label}")
    
    if "DOCUMENT" in label:
        return "document"
    
    return "chat"