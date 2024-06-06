import openai
from pinecone import Pinecone
from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import ToolException

class PineInput(BaseModel):
  """Input to get data from vector database"""
  query: str = Field(description="The query provided by the user")

def _askPine(query:str, index_name='jivaa', namespace='documents', top=3):
    try:

        pc = Pinecone()

        index = pc.Index(index_name)
        xq = openai.embeddings.create(input=[query],model="text-embedding-ada-002").data[0].embedding

        res = index.query(vector=xq, top_k=top, include_metadata=True, namespace=namespace)
        ref = res['matches'][0]['metadata']['source']
        contexts = [item['metadata']['text'] for item in res['matches']]
        augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+query

        primer = f"""You are Q&A bot. A highly intelligent system for
        a callcenterthat answers user questions based on the information
        provided by the user above. If the information can not be found
        in the information provided by the user you truthfully say "I don't know".
        """

        messages = [
            {"role": "system", "content": primer},
            {"role": "user", "content": augmented_query}
            ]

        res = openai.chat.completions.create(model="gpt-3.5-turbo",messages=messages,max_tokens=100)
        res = res.choices[0].message.content
        return f'Reference: {ref}\n{res}'
    
    except Exception as e:
        return f"An error occurred: {e}\n"


def _handle_error(error: ToolException) -> str:
  return (f"""
  The following errors occurred during tool execution:
  {error.args[0]}
  Please use an appropriate input and try again.""")

askThePine = StructuredTool.from_function(
  func=_askPine,
  name="AskPinecone",
  description="QA API for information regarding the company's documents or policies in a vector database.",
  args_schema=PineInput,
  handle_tool_error=_handle_error,
)