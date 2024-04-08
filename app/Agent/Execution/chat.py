import asyncio
import json
import re
from typing import Any, Dict, List

from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import BaseTool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.utils.function_calling import convert_to_openai_function


class TravelAgent:
  def __init__(self, prompt: BasePromptTemplate, llm: BaseChatModel, tools: List[BaseTool]):
    # TODO: Manage chat history with external db
    # TODO: Add retrievers and embeddings
    self.functions = [convert_to_openai_function(tool) for tool in tools]

    self.agent = create_react_agent(
      llm=llm,
      tools=tools,
      prompt=prompt,
    )

    self.agent_executor = AgentExecutor.from_agent_and_tools(
      agent=self.agent,
      tools=tools,
      functions=self.functions,
      verbose=False,
      handle_parsing_errors=True,
      max_iterations=3
    ).with_config(
      {"run_name": "Agent"}
    )

    self.exp = re.compile(r'^\s*//\s*')

  def run(self, input: str, chat_history: List[BaseMessage]) -> Dict[str, Any]:
    return self.agent_executor.invoke(input={
      "input": input,
      "chat_history": chat_history
    })

  async def astream(self, input: str, chat_history: List[BaseMessage]):
    ending = False

    async for data in self.agent_executor.astream_events(
      input = {
        "input": input,
        "chat_history": chat_history
      },
      version = "v1"
    ):
      event = data["event"]

      if event == "on_tool_start":
        yield json.dumps({"action": data["name"], "output": None})

      elif event == "on_tool_end":
        yield json.dumps({"action": data["name"], "output": data['data'].get('output')})
        await asyncio.sleep(0.001)

      elif event == "on_chat_model_stream":
        content = data["data"]["chunk"].content
        if ending:
          yield json.dumps({"action": "answer", "output": content})
        else:
          ending = self.exp.match(content)
          yield '{"action": null, "output": null}'

      else:
        yield '{"action": null, "output": null}'
        await asyncio.sleep(0.001)