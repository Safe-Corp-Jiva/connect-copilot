import os

tools = []

if not os.environ.get('DEV') or not os.environ.get('PRODUCTION'):
  from .sample import multiply
  tools.append(multiply)