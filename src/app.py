from fastapi import FastAPI
from src.libs.lifespan import lifespan
from src.constants import IS_TRUE

app = FastAPI(lifespan=lifespan, debug=IS_TRUE)
