from Agent import archie

def handler(event, _context):
  msg = event.get("input")
  if not msg:
    return {
      "statusCode": 400,
      "body": "Bad request"
    }
  
  chat_history = event.get("chat_history")
  if not chat_history:
    chat_history = []
  
  return {
    "statusCode": 200,
    "body": archie.run(msg, chat_history)
  }