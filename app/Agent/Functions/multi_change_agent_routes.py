import boto3, logging, openai, os

from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import ToolException

class MultiChangeAgentRoutesInput(BaseModel):
  """Input to change the routes of multiple agents"""
  query: str = Field(description="The origin and target routes to change the agents to and the number of agents.")

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_DEFAULT_REGION:
  print('AWS credentials not found.')
                                
client = boto3.client('connect',
                      region_name=AWS_DEFAULT_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def get_routes(instance_id_local, connect_client=client):
    response = connect_client.list_routing_profiles(InstanceId=instance_id_local)
    routes = {}
    for route in response['RoutingProfileSummaryList']:
        routes[route['Name']] = route['Id']
    return routes

def choose(route, possible_routes):
    xq = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that only answers the value of a key in a dictionary."},
            {"role": "user", "content": f"Choose the most simmilar route name to {route} from the ones below: {possible_routes}. Answer only the id of the chosen name."},
        ],
    )
    return xq.choices[0].message.content

def users_4_route(instance_id_local, routing_profile):
    response = client.list_users(InstanceId=instance_id_local)
    filtered_users = []

    for user_summary in response['UserSummaryList']:
        try:
            user_id = user_summary['Id']
            user_details = client.describe_user(InstanceId=instance_id_local, UserId=user_id)

            if user_details['User']['RoutingProfileId'] == routing_profile:
                user_id_val = user_details['User']['Id']
                status_response = client.get_current_user_data(InstanceId=instance_id_local,Filters={'Agents': [user_id]},)
                user_status = status_response['UserDataList'][0]['Status']['StatusName']
                
                if user_status == 'Available':
                    filtered_users.append({
                        'User': user_details['User']['Username'],
                        'Status': user_status,
                        'Id' : user_details['User']['Id']
                    })
        
        except: ...
    
    return filtered_users

def feeder(query):
    xq = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that only transforms the query into a list of 'origin route, target route, volume'. The order is paramount and you can only return the list."},
            {"role": "user", "content": f"Format the query {query}. If there is no volume value set the value to 1."},
        ],
    )
    res = xq.choices[0].message.content
    return res.split(',')

def change_route(query, instance_id_local='589e43e8-dd86-4785-8571-af7c2853adb3'):
    try:
        origin_route, target_route, volume = feeder(query)
        volume = volume.replace("'",'').strip()

        origin_routing_id = choose(origin_route,(temp:=get_routes(instance_id_local)))
        target_routing_id = choose(target_route,get_routes(instance_id_local))

        origin_name = list(temp.keys())[list(temp.values()).index(origin_routing_id)]
        target_name = list(temp.keys())[list(temp.values()).index(target_routing_id)]

        users = users_4_route(instance_id_local, origin_routing_id)
        transfers = 0
        if not users:
            return f'{origin_name} has no available users.'
        for i in range(min(int(volume), len(users))):
            try:
                response = client.update_user_routing_profile(
                    RoutingProfileId=target_routing_id,
                    UserId=users[i]['Id'],
                    InstanceId=instance_id_local,
                )
                transfers+=1
            except:
                raise Exception('An error occurred while trying to update the user routing profile.')
        return f'{transfers} agents were switched from {origin_name} to {target_name}.'
    except Exception as e:
        return f"An error occurred: {e}\n"
    
def _handle_error(error: ToolException) -> str:
  return (f"""
  The following errors occurred during tool execution:
  {error.args[0]}
  Please use an appropriate input and try again.""")

def runner(query: str):
    try:
        return change_route(query)
    except Exception as e:
        return f"An error occurred: {e}\n"

MultiChangeAgentRoutes = StructuredTool.from_function(
  func=runner,
  name="MultiChangeAgentRoutes",
  description="Change the routes of multiple agents in Amazon Connect's Callcenter.",
  args_schema=MultiChangeAgentRoutesInput,
  handle_tool_error=_handle_error,
)
