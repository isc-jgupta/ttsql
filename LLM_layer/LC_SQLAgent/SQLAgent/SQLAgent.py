from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.prompts.prompt import PromptTemplate
from sqlalchemy import create_engine

connection_string = "iris://superuser:test@localhost:2000/SDS"
db = SQLDatabase.from_uri(connection_string)

llm = OpenAI(temperature=0, verbose=True, model="gpt-3.5-turbo-instruct")
agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0, model="gpt-3.5-turbo-instruct", verbose=True),
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

Never use LIMIT statement, change to TOP.
Format all numeric response ###,###,###,###.
If the topic is not related to demographics return "SELECT 'Ask-ChatGPT'" and do not execute the query.
Whatever a question references blah blah blah what means is SDS_DataModel.Person.
Surrond literals with double-quotes in SELECT clauses.

Question: {input}"""
PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)

agent_executor.run("SELECT * FROM SDS_DataModel.Person?")