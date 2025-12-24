from graph import app

print("Pharmacy RAG Chatbot (LangGraph)")
print("Type 'exit' to quit\n")

while True:
    q = input("User: ")
    if q.lower() == "exit":
        break

    result = app.invoke({
        "query": q,
        "intent": "",
        "documents": [],
        "answer": "",
        "safety": ""
    })

    print("Bot:", result["answer"], "\n")
