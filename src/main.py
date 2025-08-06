"""App entry point
"""
from urllib.parse import urlencode, parse_qs, unquote_plus
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware

from src.app import app
from src.routes import api_router

from src.constants import IS_TRUE, ALLOWED_METHODS, ALLOWED_ORIGINS, ALLOWED_HEADERS

class URLEncodingMiddleware(BaseHTTPMiddleware):
    """Encode URL middleware
    """
    async def dispatch(self, request: Request, call_next):
        raw_query_string = request.scope["query_string"].decode()
        decoded_query_string = unquote_plus(raw_query_string.replace("&amp;", "&"))
        parsed_query = parse_qs(decoded_query_string)
        encoded_query_string = urlencode(parsed_query, doseq=True).encode()
        request.scope["query_string"] = encoded_query_string
        return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
    allow_credentials=IS_TRUE
)

app.add_middleware(URLEncodingMiddleware)

app.include_router(api_router, prefix="/mcp")

mcp = FastMCP.from_fastapi(app=app)
mcp_app = mcp.http_app(path='/mcp')
app.mount("/mcp/mcp", mcp_app)
