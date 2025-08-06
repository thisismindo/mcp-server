from src.app import app
from src.libs.db_client import CockroachDBClient

def get_db_client_rw() -> CockroachDBClient:
    return app.state.db_client_rw

def get_db_client_ro() -> CockroachDBClient:
    return app.state.db_client_ro

def get_dal(dal_class, client_getter):
    return dal_class(client_getter())
