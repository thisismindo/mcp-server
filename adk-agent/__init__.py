import os
import requests
from google.adk.agents import LlmAgent
from google.adk.tools.openapi_tool.openapi_spec_parser import OpenAPIToolset

OPENAPI_SPEC_URL: str = f"{os.getenv('MCP_SERVER_HOST')}/openapi.json"
LLM_MODEL: str = 'gemini-2.5-flash'
AGENT_NAME: str = 'user_management_agent'
AGENT_INSTRUCTION: str = 'You can manage user data by calling the available tools.'
DEFAULT_AGENT_INSTRUCTION: str = 'The user management tools are unavailable. Please check the server status.'

try:
    response = requests.get(OPENAPI_SPEC_URL)
    response.raise_for_status()
    openapi_spec_content = response.text
except requests.exceptions.RequestException:
    openapi_spec_content = None

if openapi_spec_content:
    root_agent = LlmAgent(
        model=LLM_MODEL,
        name=AGENT_NAME,
        instruction=AGENT_INSTRUCTION,
        tools=[
            OpenAPIToolset(
                spec_str=openapi_spec_content,
                spec_str_type='json'
            )
        ],
    )
else:
    root_agent = LlmAgent(
        model=LLM_MODEL,
        name=AGENT_NAME,
        instruction=DEFAULT_AGENT_INSTRUCTION,
        tools=[]
    )
