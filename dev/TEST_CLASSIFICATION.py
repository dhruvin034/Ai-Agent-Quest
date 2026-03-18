#!/usr/bin/env python3
"""
Test query classification directly
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from app.rag.query_router import classify_query

print("\n" + "="*60)
print("🧪 Query Classification Test")
print("="*60 + "\n")

test_queries = [
    "What is the invoice number?",
    "Who is the client?",
    "Extract the total amount",
    "What is the date?",
    "List all line items",
    "How are you?",
    "What time is it?",
    "Hello",
    "Can you help me find the invoice number?",
    "Tell me about the document",
]

print("Testing query classification...\n")

for query in test_queries:
    result = classify_query(query)
    symbol = "📄" if result == "document" else "💬"
    print(f"{symbol} '{query}'")
    print(f"   → Classification: {result.upper()}\n")

print("="*60)
print("✅ Test complete")
print("="*60 + "\n")
