import os
from langchain_groq import ChatGroq
from prompts import prompt
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


# Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)

# Runnable Chain 
qa_chain = prompt | llm

print("Q&A Bot - type 'exit' to quit")

while True:
    user_input = input("\nUser: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        break

    response = qa_chain.invoke({"question": user_input})
    print(f"Bot: {response.content}")
