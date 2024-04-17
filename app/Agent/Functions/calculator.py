from functools import reduce
from typing import Any, List

from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import ToolException


class MultiplicationInput(BaseModel):
  """Input for the multiplication tool, you need to provide the numbers separetly"""
  nums: Any = Field(description="A list of numbers to multiply.")

def _multiplication(nums: str | List[float | int]):
  """Multiplies a list (or pair) of numbers together."""
  if not isinstance(nums, list):
    nums = nums.strip('][').split(',')
  
  def handler(acc, val):
    try:
      val = float(val)
    except ValueError:
      try:
        val = float(val.replace("'", "").replace('"', ''))
      except ValueError:
        return acc
    
    return acc * float(val)

  return f"{reduce(handler, nums, 1.0)}\n"

def _handle_error(error: ToolException) -> str:
  return (f"""
  The following errors occurred during tool execution:
  {error.args[0]}
  Please use an appropriate input and try again.""")

# EXPORTS
multiply = StructuredTool.from_function(
  func=_multiplication,
  name="multiply",
  description="Multiplies a list (or pair) of numbers together.",
  args_schema=MultiplicationInput,
  handle_tool_error=_handle_error,
)