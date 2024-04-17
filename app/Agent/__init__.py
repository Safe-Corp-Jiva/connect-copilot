from langchain.agents import create_openai_tools_agent
from langchain_openai import ChatOpenAI

from .Execution.chat import TravelAgent
from .Functions import tools
from .Templates.proompt import prompt

_llm = ChatOpenAI(
  model="gpt-3.5-turbo-1106", 
  temperature=0.025,
  streaming=True
)

_agent = create_openai_tools_agent(_llm, tools, prompt)

archie = TravelAgent(_agent, tools)