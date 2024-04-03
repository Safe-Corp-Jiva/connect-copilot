import os

from langchain_community.chat_models import BedrockChat

from .Execution.chat import TravelAgent
from .Functions import tools
from .Templates.proompt import prompt

llm = None

if os.environ.get("DEV") or os.environ.get("PRODUCTION"):
  import boto3

  session = boto3.Session(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.environ.get("AWS_SESSION_TOKEN")
  )

  BEDROCK_CLIENT = session.client("bedrock-runtime", 'us-east-1')

  llm = BedrockChat(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0.1},
    client=BEDROCK_CLIENT
  )
else:
  llm = BedrockChat(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0.1}
  )


archie = TravelAgent(prompt, llm, tools)