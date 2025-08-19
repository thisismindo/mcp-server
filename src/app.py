import os
from fastapi import FastAPI
from src.libs.lifespan import lifespan
from src.constants import IS_TRUE

app = FastAPI(
    servers=[{
        'url': os.getenv('MCP_SERVER_HOST')
    }],
    lifespan=lifespan,
    debug=IS_TRUE
)
