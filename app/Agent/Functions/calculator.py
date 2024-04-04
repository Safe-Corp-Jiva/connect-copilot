from typing import Optional, Type

from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field


class CalculatorInput(BaseModel):
  a: int = Field(description="first number")
  b: int = Field(description="second number")

class CustomCalculatorTool(BaseTool):
  name = "Calculator"
  description = "Useful for when you need to answer questions about math"
  args_schema: Type[BaseModel] = CalculatorInput
  return_direct: bool = True

  def _run(
    self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None
  ) -> str:
    """Use the tool."""
    return a * b

  async def _arun(
    self,
    a: int,
    b: int,
    run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
  ) -> str:
    return a * b

multiply = CustomCalculatorTool()