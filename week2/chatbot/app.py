import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

from langchain_community.utilities import SQLDatabase
from langchain_core.tools import tool
from langchain_classic.agents import create_react_agent, AgentExecutor

from langchain_core.prompts import PromptTemplate

from langchain_community.tools import DuckDuckGoSearchResults


from langfuse.callback import CallbackHandler

from langchain_mongodb import MongoDBChatMessageHistory



PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "chat_memory_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "chat_history")

pg_uri = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

SESSION_ID = "user_session_1"  


#  LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)


#  mongo memory
history = MongoDBChatMessageHistory(
    connection_string=MONGO_URI,
    database_name=MONGO_DB,
    collection_name=MONGO_COLLECTION,
    session_id=SESSION_ID,
)


def format_chat_history():
    messages = history.messages

    summary = "Conversation summary not enabled."
    if len(messages) > 6:
        summary = "User and assistant have had prior discussion."

    recent = messages[-6:]

    formatted = f"Summary: {summary}\n\nRecent Conversation:\n"
    for m in recent:
        role = "User" if m.type == "human" else "Assistant"
        formatted += f"{role}: {m.content}\n"

    return formatted



db = SQLDatabase.from_uri(pg_uri)

@tool
def sql_query_tool(query: str) -> str:
    """Execute SQL query on database and return results."""
    try:
        return db.run(query)
    except Exception as e:
        return f"SQL Error: {str(e)}"

@tool
def list_tables() -> str:
    """List all tables in PostgreSQL public schema."""
    try:
        return db.run(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        )
    except Exception as e:
        return str(e)

@tool
def describe_table(table: str) -> str:
    """Describe table columns."""
    try:
        return db.run(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table}';
        """)
    except Exception as e:
        return str(e)


web_search = DuckDuckGoSearchResults(
    name="web_search",
    num_results=3
)

tools = [sql_query_tool, web_search, list_tables, describe_table]


prompt = PromptTemplate(
    input_variables=["input","tools","tool_names","agent_scratchpad","chat_history"],
    template="""
You are an intelligent assistant that can:
1) Query PostgreSQL database
2) Search the web
3) Use conversation memory

CONTEXT MEMORY:
{chat_history}

WEB RULES:
- Only call web_search max 1 time unless required.
- If answer found, STOP and answer.
- Keep response short.

DB RULES:
- Use list_tables before querying unknown tables.
- Use describe_table before using columns.
- Do NOT invent table names.

FINAL RULES:
- Use memory when helpful.
- Do not repeat actions.
- Provide clean Final Answer only.

TOOLS:
{tools}

AVAILABLE TOOL NAMES:
{tool_names}

FORMAT STRICT:
Question: {input}
Thought:
Action: one of [{tool_names}]
Action Input:
Observation:
... repeat ...
Final Answer:

Begin!
{agent_scratchpad}
"""
)


agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10
)


print("🤖 DB + Web Chatbot with Mongo MEMORY Ready (type 'exit' to quit)")


while True:
    user_input = input("\nUser: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        break

    tracer = CallbackHandler()

    try:
        chat_history_text = format_chat_history()

        result = agent_executor.invoke(
            {
                "input": user_input,
                "chat_history": chat_history_text
            },
            config={"callbacks":[tracer]}
        )

        final_answer = result["output"]
        print(f"Bot: {final_answer}")

        # SAVE MEMORY
        history.add_user_message(user_input)
        history.add_ai_message(final_answer)

        tracer.flush()

    except Exception as e:
        print("Bot: Something went wrong.", e)
        tracer.flush()
