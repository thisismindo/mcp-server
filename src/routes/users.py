"""Users router
"""
from typing import Optional, List
from fastapi import APIRouter, status, Depends, Query
from fastapi.responses import JSONResponse
from src.models.user import CreateUser, UpdateUser, UserResponse, SignupResponse, \
    UserDefaultResponse, UpdateUserResponse
from src.models.user_dal import UserDAL
from src.dependencies import get_dal, get_db_client_rw, get_db_client_ro
from src.helpers.common import custom_serializer
from src.constants import IS_TRUE, IS_FALSE, GET_USERS_OP_ID, GET_USER_OP_ID, \
    POST_USER_SIGNUP_OP_ID, PUT_USER_OP_ID, DELETE_USER_OP_ID, USERS

class UsersRouter:
    """Users router class
    """
    def __init__(self):
        """Initialize this class and define class member(s)
        """
        self.router: APIRouter = APIRouter()

        self.router.add_api_route("/", self.get_users, methods=["GET"], operation_id=GET_USERS_OP_ID,
                                  tags=[USERS], response_model=List[UserResponse])
        self.router.add_api_route("/{id}", self.get_user, methods=["GET"], operation_id=GET_USER_OP_ID,
                                  tags=[USERS], response_model=UserResponse)
        self.router.add_api_route("/", self.signup, methods=["POST"], operation_id=POST_USER_SIGNUP_OP_ID,
                                  tags=[USERS], response_model=SignupResponse)
        self.router.add_api_route("/{id}", self.update_user, methods=["PUT"], operation_id=PUT_USER_OP_ID,
                                  tags=[USERS], response_model=UpdateUserResponse)
        self.router.add_api_route("/{id}", self.delete_user, methods=["DELETE"], operation_id=DELETE_USER_OP_ID,
                                  tags=[USERS], response_model=UserDefaultResponse)

    async def _get_user_data(self, dal: UserDAL, user_id: str):
        """Core logic to retrieve and serialize user data.
        """
        query_result = await dal.get_user(id=user_id)
        if query_result:
            mutable_result = dict(query_result[0])
            mutable_result['id'] = custom_serializer(mutable_result['id'])
            mutable_result['created_at'] = custom_serializer(mutable_result['created_at'])
            mutable_result['updated_at'] = custom_serializer(mutable_result['updated_at'])
            return mutable_result
        return None

    async def signup(self, user: CreateUser,
                     dal: UserDAL = Depends(lambda: get_dal(UserDAL, get_db_client_rw))
                ):
        """Sign up new user
        """
        new_user_uuid = await dal.new_user(user=user)
        user_data = await self._get_user_data(dal=dal, user_id=new_user_uuid)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': IS_TRUE,
                'message': [],
                'response': user_data
            }
        )

    async def get_user(self, id: str,
                       dal: UserDAL = Depends(lambda: get_dal(UserDAL, get_db_client_ro))
                    ):
        """Get user
        """
        query_result = await self._get_user_data(dal=dal, user_id=id)
        if not query_result:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    'status': IS_FALSE,
                    'message': [],
                    'response': query_result
                }
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': IS_TRUE,
                'message': [],
                'response': query_result
            }
        )

    async def get_users(self, offset: Optional[int] = Query(0),
                        limit: Optional[int] = Query(1),
                        dal: UserDAL = Depends(lambda: get_dal(UserDAL, get_db_client_ro))
                    ):
        """Get users
        """
        response: List = []
        query_results = await dal.get_users(offset=offset, limit=limit)
        if query_results:
            for query_result in query_results:
                mutable_result = dict(query_result)
                mutable_result['id'] = custom_serializer(mutable_result['id'])
                mutable_result['created_at'] = custom_serializer(mutable_result['created_at'])
                mutable_result['updated_at'] = custom_serializer(mutable_result['updated_at'])
                response.append(mutable_result)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': IS_TRUE,
                'message': [],
                'response': response
            }
        )

    async def update_user(self, user: UpdateUser,
                     dal: UserDAL = Depends(lambda: get_dal(UserDAL, get_db_client_rw))
                ):
        """Update user
        """
        await dal.update_user(user=user)
        user_data = await self._get_user_data(dal=dal, user_id=user.id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': IS_TRUE,
                'message': [],
                'response': user_data
            }
        )

    async def delete_user(self, id: str,
                     dal: UserDAL = Depends(lambda: get_dal(UserDAL, get_db_client_rw))
                ):
        """Delete user
        """
        errors: List = []
        if not id:
            errors.append('user id is required.')
        if len(errors):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    'status': IS_FALSE,
                    'message': errors,
                    'response': {}
                }
            )

        await dal.delete_user(id=id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': IS_TRUE,
                'message': [],
                'response': {}
            }
        )
