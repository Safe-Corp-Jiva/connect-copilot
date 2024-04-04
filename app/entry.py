from typing import Any, Dict

from Agent import archie
from definitions import LambdaContext


def handler(event: Dict[str, Any], _context: LambdaContext) -> Dict[str, Any]:
  msg = event.get("input")
  if not msg:
    return {
      "statusCode": 400,
      "body": "Bad request"
    }
  
  chat_history = event.get("chat_history", [])

  return {
    "statusCode": 200,
    "body": archie.run(msg, chat_history)
  }