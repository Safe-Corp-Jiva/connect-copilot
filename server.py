import os

from typing import Annotated

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from Agent import archie

client = None

if os.environ.get("LANGCHAIN_TRACING_V2"):
  from langsmith import Client
  client = Client()

app = FastAPI(
  title="ArchieAPI",
  version="1.0",
  description="A simple API server to interact with Archie.",
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
  expose_headers=["*"],
)

@app.get("/heartbeat", response_class=ORJSONResponse)
def health():
  return ORJSONResponse({"status": "ok"})

class ChatRequest(BaseModel):
  input: str = Field(..., title="Input", description="The input to Archie.")
  chat_history: Annotated[list, Field(..., title="Chat History", description="The chat history to Archie.")]

@app.post("/chat", response_class=ORJSONResponse)
async def chat(req: ChatRequest):
  return ORJSONResponse({
    "output": archie.run(req.input, req.chat_history)
  })

if __name__ == "__main__":
  import uvicorn

  uvicorn.run(
    app, 
    host="0.0.0.0",
    port=8000,
    proxy_headers=True
  )