import requests
import os
from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import ToolException

FLIGHT_API_URL = os.getenv("FLIGHT_API_URL", "http://localhost:8080/api")

class FlightInput(BaseModel):
  """Input to get Flight data from a private API"""
  id: str = Field(description="The flight ID to get data for.")

def _getFlights(id: str | int):
  """
  Given the id of a flight this tool returns a JSON object containing the following flight data:
  {
    "id": number,
    "origin": {
      "icao": string,
      "iata": string,
      "name": string,
      "state": string,
      "country": string
    },
    "destination": {
      "icao": string,
      "iata": string,
      "name": string,
      "state": string,
      "country": string
    },
    "arrival": timestamp,
    "departure": timestamp
  }
  """
  try:
    req = requests.get(f"{FLIGHT_API_URL}/flights/{id}")
    req.raise_for_status()
    return req.json()
  except requests.exceptions.RequestException as e:
    return f"An error occurred: {e}\n"
  except Exception as e:
    return f"An error occurred: {e}\n"
  
def _getFlightSeats(id: str | int):
  """
  Given the id of a flight this tool returns a JSON object containing the available seats for the flight:
  {
    "seats": {
      "number": string,
      "class": ECONOMY | BUSINESS | FIRST,
      "price": number
    }
  }  
  """
  try:
    req = requests.get(f"{FLIGHT_API_URL}/flights/{id}/seats")
    req.raise_for_status()
    return req.json()
  except requests.exceptions.RequestException as e:
    return f"An error occurred: {e}\n"

def _handle_error(error: ToolException) -> str:
  return (f"""
  The following errors occurred during tool execution:
  {error.args[0]}
  Please use an appropriate input and try again.""")

flights = StructuredTool.from_function(
  func=_getFlights,
  name="GetFlights",
  args_schema=FlightInput,
  handle_tool_error=_handle_error,
)

seats = StructuredTool.from_function(
  func=_getFlightSeats,
  name="GetFlightSeats",
  args_schema=FlightInput,
  handle_tool_error=_handle_error,
)