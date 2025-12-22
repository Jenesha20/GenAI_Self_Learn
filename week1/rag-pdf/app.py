from ingest import ingest_pdf
from rag_chain import build_rag_chain

PDF_PATH = "./data/sample.pdf"

print("Ingesting PDF...")
ingest_pdf(PDF_PATH)

rag_chain = build_rag_chain()

print("PDF Q&A Bot (Groq) — type 'exit' to quit")

while True:
    query = input("\nUser: ")

    if query.lower() in ["exit", "quit"]:
        break

    answer = rag_chain.run(query)
    print(f"Bot: {answer}")
