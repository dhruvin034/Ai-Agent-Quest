from graph.rag_graph import rag_graph
from ingest.pdf_ingest import ingest_documents
import os

# PDF_PATH = r"D:\Ai_Rag_Quest\data\demo-invoice-20tax-8.pdf"

# Fix Windows path
VECTOR_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "vector_storage")
VECTOR_DB_PATH = os.path.abspath(VECTOR_DB_PATH)


def main():

    print("\n📄 Conversational RAG System Ready")
    print("Type 'exit' to quit\n")

    while True:

        question = input("Ask a question: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("\nGoodbye 👋")
            break

        if not question:
            print("Please enter a question.")
            continue

        result = rag_graph.invoke({
            "question": question
        })
        
        print("\n Tool:\n")
        print(result['route'])

        print("\n💡 Answer:\n")
        print(result["answer"])

        if "sources" in result and result["sources"]:
            print("\n📚 Sources:")
            for s in result["sources"]:
                print(f"- {s}")

        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":

    # Index PDF only if vector DB does not exist
    if not os.path.exists(VECTOR_DB_PATH):
        print(f"📥 Indexing PDF documents from data folder...")
        ingest_documents()
        print(f"✅ Vector DB created at {VECTOR_DB_PATH}")
    else:
        print(f"✅ Vector DB found at {VECTOR_DB_PATH}")

    main()