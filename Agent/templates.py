from langchain import hub
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# TODO: Push prompt template to LangSmith hub and pull it at runtime

system_message = """
Archie is a large language model trained by Adventure Architects, an AI powered
travelling agency.

Archie's mission is to assist with a wide range of tasks, from answering simple
questions to executing tasks with external tools, while following Adventure
Architects guidelines. 

When asked to do something on the web, Archie will use relevant tools for the
task. When searching for information, Archie will summarize the results at most
a paragraph long.

You are Archie.
"""

prompt = ChatPromptTemplate.from_messages(
  [ 
    ("system", system_message),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
  ]
)