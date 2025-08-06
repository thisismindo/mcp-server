"""User DAL
"""
from typing import Tuple, Dict
from src.constants import IS_TRUE, IS_FALSE

class UserDAL:
    """User Data Access Layer class
    """
    def __init__(self, db_client):
        """Initialze this class and assign class member(s)
        """
        self.db_client = db_client

    async def new_user(self, user: Dict):
        """Create new user
        """
        sql_query: str = """
            INSERT INTO
                users
            (username, email_address, active)
            VALUES
            ($1, $2, $3)
            RETURNING id
        """
        values: Tuple = tuple([
            user.username,
            user.email_address,
            user.active
        ])
        try:
            result = await self.db_client.execute_write(sql_query, *values)
            return str(result[0]["id"])
        except Exception as e:
            raise RuntimeError(f"Failed to create user: {str(e)}")

    async def get_user(self, id: str):
        """Get user
        """
        sql_query: str = """
            SELECT
                id,
                username,
                email_address,
                created_at,
                updated_at
            FROM
                users
            WHERE
                id = $1
            AND
                active = $2
            LIMIT $3
        """
        values: Tuple = tuple([
            id,
            IS_TRUE,
            1
        ])
        query_result: Dict = {}
        try:
            query_result = await self.db_client.execute_read(sql_query, *values)
        except Exception as e:
            raise RuntimeError(f"Failed to get user: {str(e)}")

        return query_result

    async def get_users(self, offset: int, limit: int):
        """Get users
        """
        sql_query: str = """
            SELECT
                id,
                username,
                email_address,
                created_at,
                updated_at
            FROM
                users
            WHERE
                active = $1
            LIMIT $2
            OFFSET $3
        """
        values: Tuple = tuple([
            IS_TRUE,
            limit,
            offset
        ])
        try:
            return await self.db_client.execute_read(sql_query, *values)
        except Exception as e:
            raise RuntimeError(f"Failed to get users: {str(e)}")

    async def update_user(self, user: Dict):
        """Update user
        """
        sql_query: str = """
            UPSERT INTO
                users
            (id, email_address)
            VALUES
            ($1, $2)
        """
        values: Tuple = tuple([
            user.id,
            user.email_address
        ])
        try:
            await self.db_client.execute_write(sql_query, *values)
        except Exception as e:
            raise RuntimeError(f"Failed to update user: {str(e)}")

    async def delete_user(self, id: str):
        """Update user
        """
        sql_query: str = """
            UPDATE
                users
            SET
                active = $1
            WHERE
                id = $2
        """
        values: Tuple = tuple([
            IS_FALSE,
            id
        ])
        try:
            await self.db_client.execute_write(sql_query, *values)
        except Exception as e:
            raise RuntimeError(f"Failed to delete user: {str(e)}")
