import os
from typing import Annotated, Dict, List

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from Agent import archie

app = FastAPI()

class ChatRequest(BaseModel):
  input: str = Field(..., title="Input", description="The input to Archie.")
  chat_history: Annotated[List[Dict[str, str]], 
                          Field(..., 
                                title="Chat History", 
                                description="The chat history for Archie.")]

@app.post("/", response_class=ORJSONResponse)
async def chat(req: ChatRequest):
  return ORJSONResponse({
    "message": archie.run(
      input=req.input,
      chat_history=req.chat_history)})

if __name__ == "__main__":
  uvicorn.run(
    app,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8080"))
  )