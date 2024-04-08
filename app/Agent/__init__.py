from langchain_community.chat_models import BedrockChat

from .Execution.chat import TravelAgent
from .Functions import tools
from .Templates.proompt import prompt

llm = BedrockChat(
  model_id="anthropic.claude-3-sonnet-20240229-v1:0",
  model_kwargs={"temperature": 0.1},
  streaming=True
)

archie = TravelAgent(prompt, llm, tools)