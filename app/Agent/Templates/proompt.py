# TODO: Push prompt template to LangSmith hub and pull it at runtime
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

system = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
//Final Answer: The final answer to the question or the result from a tool (Start with double slash //)

Begin!'''

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", '''{input}'''),
        ("ai", '''{agent_scratchpad}'''),
    ]
)