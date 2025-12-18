from langchain_core.prompts import PromptTemplate

# Prompt Template
prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are a clear and precise AI assistant.

Answer the following question in a concise and understandable way.

Question:
{question}

Answer:
"""
)