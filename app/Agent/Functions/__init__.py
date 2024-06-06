from .flight_api import flights, seats
from .searching import search
from .askPine_api import askThePine
from .multi_change_agent_routes import MultiChangeAgentRoutes

tools = [
  MultiChangeAgentRoutes,
  askThePine,
  flights,
  search,
  seats,
]
