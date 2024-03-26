from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain_community.tools.tavily_search import TavilySearchResults


from Agent.chat import agent_executor as travel_agent

app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
  expose_headers=["*"],
)

add_routes(
  app,
  travel_agent,
  path="/agent",
)

if __name__ == "__main__":
  import uvicorn

  print(TavilySearchResults(query="What is tavily"))
  uvicorn.run(
    app, 
    host="0.0.0.0",
    port=8000
  )