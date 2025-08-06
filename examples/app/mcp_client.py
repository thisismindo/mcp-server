"""
MCP Client for interacting with the MCP server based on OpenAPI specification.
"""
import httpx
from typing import List
from app.user_model import StatusResponse, UpdateUser, UserDefaultResponse, \
    UserResponse, CreateUser, SignupResponse, UpdateUserResponse
from app.constants import MCP_BASE_URL

class MCPClient:
    def __init__(self, base_url: str = MCP_BASE_URL):
        """
        Initialize this class and assign class member(s)
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def close(self):
        """
        Close transport
        """
        await self.client.aclose()

    async def get_status(self) -> StatusResponse:
        """
        Get MCP server status
        """
        url = f"{self.base_url}/status/"
        response = await self.client.get(url)
        response.raise_for_status()
        return StatusResponse(**response.json())

    async def get_users(self, offset: int = 0, limit: int = 100) -> List[UserResponse]:
        """
        Get users with pagination
        """
        url = f"{self.base_url}/users/"
        params = {"offset": offset, "limit": limit}
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return [UserResponse(**user) for user in data.get("response", [])]

    async def create_user(self, username: str, email_address: str, active: bool = True) -> SignupResponse:
        """
        Create a new user
        """
        url = f"{self.base_url}/users/"
        data = CreateUser(username=username, email_address=email_address, active=active)
        response = await self.client.post(url, json=data.model_dump())
        print(response)
        response.raise_for_status()
        return SignupResponse(**response.json())

    async def get_user(self, user_id: str) -> UserResponse:
        """
        Get user by ID
        """
        url = f"{self.base_url}/users/{user_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        data = response.json()
        return UserResponse(**data.get("response", {}))

    async def update_user(self, user_id: str, email_address: str) -> UpdateUserResponse:
        """
        Update user email address
        """
        url = f"{self.base_url}/users/{user_id}"
        data = UpdateUser(id=user_id, email_address=email_address)
        response = await self.client.put(url, json=data.model_dump())
        response.raise_for_status()
        return UpdateUserResponse(**response.json())

    async def delete_user(self, user_id: str) -> UserDefaultResponse:
        """
        Delete user by ID
        """
        url = f"{self.base_url}/users/{user_id}"
        response = await self.client.delete(url)
        response.raise_for_status()
        return UserDefaultResponse(**response.json())

mcp_client = MCPClient()
