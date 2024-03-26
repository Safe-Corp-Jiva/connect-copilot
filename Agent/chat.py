from typing import Any, List, Union

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import \
    format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import \
    OpenAIToolsAgentOutputParser
from langchain_core.messages import AIMessage, FunctionMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langserve.pydantic_v1 import BaseModel, Field

from .Functions import tools
from .templates import prompt

llm = ChatOpenAI()
tuned_llm = llm.bind_tools(tools)

# TODO: Manage chat history with external db
# TODO: Add retrievers and embeddings

agent = (
  {
    "input": lambda x: x["input"],
    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
        x["intermediate_steps"]
    ),
    "chat_history": lambda x: x["chat_history"],
  }
  | prompt
  | tuned_llm
  | OpenAIToolsAgentOutputParser()
)

class Input(BaseModel):
  input: str
  chat_history: List[Union[HumanMessage, AIMessage, FunctionMessage]] = Field(
    ...,
    extra={
      "widget": {
        "type": "chat", 
        "input": "input", 
        "output": "output"
      }
    }
  )

class Output(BaseModel):
    output: Any

agent_executor = AgentExecutor(
  agent=agent,
  tools=tools,
  verbose=True
).with_types(
  input_type=Input,
  output_type=Output
).with_config(
  {"run_name": "agent"}
)