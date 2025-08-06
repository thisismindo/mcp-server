"""CockroachDB client
"""
import asyncpg
from enum import Enum
from src.constants import DB_POOL_DEFAULT_MIN_SIZE, DB_POOL_DEFAULT_MAX_SIZE

class DBAccessMode(Enum):
    """DB access mode definitions
    """
    READ = "READ"
    WRITE = "WRITE"
    BOTH = "BOTH"

class CockroachDBClient:
    """CockroachDBClient class
    """
    def __init__(
        self,
        ssl: str | None = None,
        ro_dsn: str | None = None,
        rw_dsn: str | None = None,
        mode: DBAccessMode = DBAccessMode.BOTH,
        min_size: int = DB_POOL_DEFAULT_MIN_SIZE,
        max_size: int = DB_POOL_DEFAULT_MAX_SIZE
    ):
        """Initialize this class and set class members
        """
        self.ssl = ssl
        self.ro_dsn = ro_dsn
        self.rw_dsn = rw_dsn
        self.mode = mode
        self.min_size = min_size
        self.max_size = max_size
        self.ro_pool = None
        self.rw_pool = None

    async def connect(self):
        """Connect DB
        """
        if self.mode in (DBAccessMode.READ, DBAccessMode.BOTH) and self.ro_dsn:
            self.ro_pool = await asyncpg.create_pool(
                dsn=self.ro_dsn, min_size=self.min_size, max_size=self.max_size, ssl=self.ssl
            )
        if self.mode in (DBAccessMode.WRITE, DBAccessMode.BOTH) and self.rw_dsn:
            self.rw_pool = await asyncpg.create_pool(
                dsn=self.rw_dsn, min_size=self.min_size, max_size=self.max_size, ssl=self.ssl
            )

    async def disconnect(self):
        """Disconnect DB
        """
        if self.ro_pool:
            await self.ro_pool.close()
        if self.rw_pool:
            await self.rw_pool.close()

    async def execute_read(self, query: str, *args):
        """Perform read operation
        """
        if self.ro_pool:
            async with self.ro_pool.acquire() as conn:
                return await conn.fetch(query, *args)
        elif self.rw_pool:
            async with self.rw_pool.acquire() as conn:
                return await conn.fetch(query, *args)
        else:
            raise RuntimeError("No connection pool (read-only or read-write) is initialized.")

    async def execute_write(self, query: str, *args):
        """Perform write operation
        """
        if not self.rw_pool:
            raise RuntimeError("Write pool not initialized.")
        async with self.rw_pool.acquire() as conn:
            if "RETURNING" in query.upper():
                return await conn.fetch(query, *args)
            return await conn.execute(query, *args)
