import json
from typing import Any, Dict, List

from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.agents.agent_iterator import AgentExecutorIterator
from langchain.tools import BaseTool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts.base import BasePromptTemplate


class TravelAgent:
  def __init__(self, prompt: BasePromptTemplate, llm: BaseChatModel, tools: List[BaseTool]):
    # TODO: Manage chat history with external db
    # TODO: Add retrievers and embeddings
    
    self.agent = create_structured_chat_agent(
      llm=llm,
      tools=tools,
      prompt=prompt,
    )

    self.agent_executor = AgentExecutor.from_agent_and_tools(
      agent=self.agent,
      tools=tools,
      verbose=False,
      handle_parsing_errors=True
    )

  def run(self, input: str, chat_history: List[BaseMessage]) -> Dict[str, Any]:
    return self.agent_executor.invoke(input={
      "input": input,
      "chat_history": chat_history
    })

  async def astream(self, input: str, chat_history: List[BaseMessage]):
    raise NotImplementedError()

    # Not streaming (waits for full output) ¯\_(°_°)_/¯
    iterator = AgentExecutorIterator(
      self.agent_executor,
      { "input": input,
        "chat_history": chat_history},
      yield_actions=False,
    )
    
    async for chunk in iterator:
      if "output" in chunk:
        yield json.dumps({"output": chunk["output"]})

    # Neither does self.agent_executor.astream (maybe its Bedrock...)
