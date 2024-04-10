import asyncio
import json
import random
from typing import Any, Dict, List

from langchain.agents import AgentExecutor
from langchain.tools import BaseTool
from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage

class TravelAgent:
  def __init__(self, agent: Runnable, tools: List[BaseTool]):
    # TODO: Manage chat history with external db
    # TODO: Add retrievers and embeddings
    self.agent = agent
    self.agent_executor = AgentExecutor.from_agent_and_tools(
      agent=self.agent,
      tools=tools,
      verbose=False,
      handle_parsing_errors=True,
      max_iterations=3
    ).with_config(
      {"run_name": "Agent"}
    )

  def run(self, input: str, chat_history: List[BaseMessage]) -> Dict[str, Any]:
    return self.agent_executor.invoke(input={
      "input": input,
      "chat_history": chat_history
    })

  async def astream(self, input: str, chat_history: List[BaseMessage]):
    async for data in self.agent_executor.astream_events(
      input = {
        "input": input,
        "chat_history": chat_history
      },
      version = "v1"
    ):
      event = data["event"]
      
      if event == "on_tool_start":
        yield json.dumps({"action": data["name"], 
                          "output": None})

      elif event == "on_tool_end":
        yield json.dumps({"action": data["name"], 
                          "output": "Processing Results\n"})
        await asyncio.sleep(0.001)

      elif event == "on_chat_model_stream":
        content = data["data"]["chunk"].content
        if content:
          yield json.dumps({"action": "response", 
                            "output": content})
        else:
          yield '{"action": null, "output": null}'

      else:
        yield '{"action": null, "output": null}'
        await asyncio.sleep(0.001)
    
    end = ["🤖", "💻", "😄", "😊", "⚡", "👋", "🫡", "🚀", "🛩️", "🧳"]

    yield f'{{"action": "answer", "output": "{random.choice(end)}\\n" }}'