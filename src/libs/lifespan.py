import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.libs.db_client import CockroachDBClient, DBAccessMode
from src.constants import DB_RO_VAR, DB_RW_VAR

db_client_ro = CockroachDBClient(
    ro_dsn=os.getenv(DB_RO_VAR),
    mode=DBAccessMode.READ
)

db_client_rw = CockroachDBClient(
    rw_dsn=os.getenv(DB_RW_VAR),
    mode=DBAccessMode.WRITE
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager to manage resources.
    """
    app.state.db_client_ro = db_client_ro
    app.state.db_client_rw = db_client_rw

    await db_client_ro.connect()
    await db_client_rw.connect()

    try:
        yield
    finally:
        await db_client_ro.disconnect()
        await db_client_rw.disconnect()
        del app.state.db_client_ro
        del app.state.db_client_rw
