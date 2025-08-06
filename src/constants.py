from typing import List

# COMMON
IS_TRUE: bool = True
IS_FALSE: bool = False

# DB
DB_POOL_DEFAULT_MIN_SIZE: int = 1
DB_POOL_DEFAULT_MAX_SIZE: int = 15
DB_RO_VAR: str = 'DATABASE_RO_DSN'
DB_RW_VAR: str = 'DATABASE_RW_DSN'

# MCP Tags
GET_API_STATUS_OP_ID: str = 'get_api_status'
GET_USER_OP_ID: str = 'get_user'
GET_USERS_OP_ID: str = 'get_users'
POST_USER_SIGNUP_OP_ID: str = 'post_user_signup'
PUT_USER_OP_ID: str = 'put_user'
DELETE_USER_OP_ID: str = 'delete_user'

USER_OPERATIONS: List = [
    GET_USER_OP_ID,
    GET_USERS_OP_ID,
    POST_USER_SIGNUP_OP_ID,
    PUT_USER_OP_ID,
    DELETE_USER_OP_ID
]

STATUS_OPERATIONS: List = [
    GET_API_STATUS_OP_ID,
]

# CORS
ALLOWED_ORIGINS: List = [
    "http://localhost",
    "http://127.0.0.1"
]
ALLOWED_METHODS: List = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS"
]
ALLOWED_HEADERS: List = [
    "Authorization",
    "Access-Control-Allow-Origin",
    "Content-Security-Policy",
    "Content-Type",
    "Accept",
    "Accept-Language",
    "Accept-Encoding",
    "Connection",
    "Range",
    "Origin",
    "Access-Control-Request-Method"
]
