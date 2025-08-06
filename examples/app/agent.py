"""
Agent logic for handling user queries using LLM and MCP server as tools.
"""
import re
import asyncio
from typing import Dict, Any
from app.mcp_client import mcp_client

class MockLLM:
    """
    Mock LLM for processing queries and selecting tools
    """

    def __init__(self):
        """
        Initialize this class and assign class member(s)
        """
        self.tools = {
            "get_status": "Check MCP server status",
            "list_users": "Get all users with pagination",
            "create_user": "Create a new user with username and email",
            "get_user": "Get user by ID",
            "update_user": "Update user email address",
            "delete_user": "Delete user by ID"
        }

    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze user query and determine intent and parameters
        """
        query_lower = query.lower()

        if any(word in query_lower for word in ["status", "health", "running", "up"]):
            return {
                "intent": "get_status",
                "parameters": {},
                "confidence": 0.9
            }

        if any(word in query_lower for word in ["list", "show", "get", "all"]):
            offset = 0
            limit = 100
            if "first" in query_lower or "start" in query_lower:
                offset = 0
            if "limit" in query_lower:
                limit_match = re.search(r'limit\s*(\d+)', query_lower)
                if limit_match:
                    limit = int(limit_match.group(1))

            return {
                "intent": "list_users",
                "parameters": {"offset": offset, "limit": limit},
                "confidence": 0.8
            }

        if any(word in query_lower for word in ["create", "add", "new", "signup", "register"]):
            username = None
            email = None

            username_match = re.search(r'username[:\s]+([a-zA-Z0-9_]+)', query_lower)
            if username_match:
                username = username_match.group(1)

            email_match = re.search(r'email[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', query_lower)
            if email_match:
                email = email_match.group(1)

            if username and email:
                return {
                    "intent": "create_user",
                    "parameters": {"username": username, "email_address": email},
                    "confidence": 0.9
                }
            else:
                return {
                    "intent": "create_user",
                    "parameters": {"username": "default_user", "email_address": "default@example.com"},
                    "confidence": 0.7
                }

        if any(word in query_lower for word in ["find", "get", "user", "by", "id"]):
            id_match = re.search(r'id[:\s]+([a-f0-9-]+)', query_lower)
            if id_match:
                user_id = id_match.group(1)
                return {
                    "intent": "get_user",
                    "parameters": {"user_id": user_id},
                    "confidence": 0.8
                }

        if any(word in query_lower for word in ["update", "change", "modify", "edit"]):
            id_match = re.search(r'id[:\s]+([a-f0-9-]+)', query_lower)
            email_match = re.search(r'email[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', query_lower)

            if id_match and email_match:
                return {
                    "intent": "update_user",
                    "parameters": {
                        "user_id": id_match.group(1),
                        "email_address": email_match.group(1)
                    },
                    "confidence": 0.8
                }

        if any(word in query_lower for word in ["delete", "remove", "drop"]):
            id_match = re.search(r'id[:\s]+([a-f0-9-]+)', query_lower)
            if id_match:
                return {
                    "intent": "delete_user",
                    "parameters": {"user_id": id_match.group(1)},
                    "confidence": 0.8
                }

        return {
            "intent": "unknown",
            "parameters": {},
            "confidence": 0.1
        }

    def generate_response(self, intent: str, result: Any) -> str:
        """
        Generate natural language response based on intent and result
        """
        if intent == "get_status":
            if result.status:
                return f"MCP Server Status: {', '.join(result.message)}"
            else:
                return "MCP Server is not responding properly"

        elif intent == "list_users":
            if result:
                user_list = "\n".join([
                    f"• {user.username} ({user.email_address}) - ID: {user.id}"
                    for user in result
                ])
                return f"Found {len(result)} users:\n{user_list}"
            else:
                return "No users found"

        elif intent == "create_user":
            if result.status:
                user = result.response
                return f"User created successfully!\nUsername: {user.username}\nEmail: {user.email_address}\nID: {user.id}"
            else:
                return "Failed to create user"

        elif intent == "get_user":
            if result:
                return f"User Details:\nUsername: {result.username}\nEmail: {result.email_address}\nID: {result.id}\nCreated: {result.created_at}"
            else:
                return "User not found"

        elif intent == "update_user":
            if result.status:
                user = result.response
                return f"User updated successfully!\nUsername: {user.username}\nNew Email: {user.email_address}\nID: {user.id}"
            else:
                return "Failed to update user"

        elif intent == "delete_user":
            if result.status:
                return "User deleted successfully!"
            else:
                return "Failed to delete user"

        elif intent == "unknown":
            return "I'm not sure what you want to do. Try asking me to:\n• Check server status\n• List users\n• Create a user\n• Get user by ID\n• Update user email\n• Delete a user"

        return "Unexpected response"

class Agent:
    def __init__(self):
        self.llm = MockLLM()

    async def process_query(self, query: str) -> str:
        """
        Process user query using LLM and MCP tools
        """
        try:
            analysis = self.llm.analyze_query(query)
            intent = analysis["intent"]
            parameters = analysis["parameters"]

            if intent == "get_status":
                result = await mcp_client.get_status()
            elif intent == "list_users":
                result = await mcp_client.get_users(
                    offset=parameters.get("offset", 0),
                    limit=parameters.get("limit", 100)
                )
            elif intent == "create_user":
                result = await mcp_client.create_user(
                    username=parameters["username"],
                    email_address=parameters["email_address"]
                )
            elif intent == "get_user":
                result = await mcp_client.get_user(parameters["user_id"])
            elif intent == "update_user":
                result = await mcp_client.update_user(
                    user_id=parameters["user_id"],
                    email_address=parameters["email_address"]
                )
            elif intent == "delete_user":
                result = await mcp_client.delete_user(parameters["user_id"])
            else:
                result = None

            return self.llm.generate_response(intent, result)

        except Exception as e:
            return f"Error processing query: {str(e)}"

agent = Agent()

def process_query(query: str) -> str:
    """
    Synchronous wrapper for async process_query
    """
    return asyncio.run(agent.process_query(query))
