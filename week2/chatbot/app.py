import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_core.tools import tool
# from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import create_react_agent, AgentExecutor

from langchain_core.prompts import PromptTemplate

from langchain_community.tools import DuckDuckGoSearchResults
from langfuse.callback import CallbackHandler

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")

pg_uri = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

#LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)


# SQL TOOL
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
    """List all tables in the PostgreSQL public schema."""
    try:
        return db.run(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        )
    except Exception as e:
        return str(e)


@tool
def describe_table(table: str) -> str:
    """Describe table columns to understand structure."""
    try:
        return db.run(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table}';
        """)
    except Exception as e:
        return str(e)


# WEB SEARCH TOOL
web_search = DuckDuckGoSearchResults(
    name="web_search",
    num_results=3
)
tools = [sql_query_tool, web_search, list_tables, describe_table]
prompt = PromptTemplate(
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
    template="""
You are an intelligent assistant that can:
1) Query PostgreSQL database
2) Search the web

WEB RULES:
- Only call web_search at most 1 time unless absolutely required.
- If web result clearly contains answer, STOP and answer.
- Extract only needed info (short sentence).
- Don't repeat searches.

DB RULES:
- Use list_tables before querying unknown tables.
- Use describe_table to understand columns.
- Then query meaningfully.
- Do NOT invent table names.

FINAL RULES:
- No unnecessary repeated actions.
- Stop when answer found.
- Provide clean Final Answer only.

TOOLS:
{tools}

AVAILABLE TOOL NAMES:
{tool_names}

FORMAT:
Question: {input}
Thought:
Action: one of [{tool_names}]
Action Input:
Observation:
... repeat...
Final Answer:

Begin!
{agent_scratchpad}
"""
)



# REACT AGENT
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


print("DB + Web Chatbot Ready (type 'exit' to quit)")

while True:
    user_input = input("\nUser: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        break

   # Langfuse tracer
    tracer = CallbackHandler()

    try:
        result = agent_executor.invoke(
            {"input": user_input},
            config={"callbacks": [tracer]}
        )

        final_answer = result["output"]
        print(f"Bot: {final_answer}")

        tracer.flush()   # ensures data is sent
    except Exception as e:
        print("Bot: Something went wrong.")
        tracer.flush()
        raise e



