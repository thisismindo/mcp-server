"""Status router
"""
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.models.status import StatusResponse
from src.constants import IS_TRUE
from src.constants import GET_API_STATUS_OP_ID, HEALTHCHECK

class StatusRouter:
    """Status router class
    """
    def __init__(self):
        """Initialize and define class members for this class
        """
        self.router: APIRouter = APIRouter()

        self.router.add_api_route("/", self.get_mcp_server_status, methods=["GET"], operation_id=GET_API_STATUS_OP_ID, tags=[HEALTHCHECK], response_model=StatusResponse)

    async def get_mcp_server_status(self):
        """Get MCP Server Status
        """
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': IS_TRUE,
                'message': [
                    "MCP Server is up and running"
                ],
                'response': {}
            }
        )
