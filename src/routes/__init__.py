"""App Main Routes
"""
from fastapi import APIRouter
from src.routes.status import StatusRouter
from src.routes.users import UsersRouter

api_router = APIRouter()

status_router: StatusRouter = StatusRouter()
users_router: UsersRouter = UsersRouter()

api_router.include_router(
    status_router.router,
    prefix="/status",
    include_in_schema=True
)

api_router.include_router(
    users_router.router,
    prefix="/users",
    include_in_schema=True
)
