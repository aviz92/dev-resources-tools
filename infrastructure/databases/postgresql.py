import logging
import os
from typing import Optional
import psycopg2
from psycopg2 import extras


class PostgreSQL:
    def __init__(
        self,
        name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.name = name or os.getenv("POSTGRESQL_NAME")
        self.host = host or os.getenv("POSTGRESQL_HOST")
        self.port = port or os.getenv("POSTGRESQL_PORT")
        self.username = username or os.getenv("POSTGRESQL_USERNAME")
        self.password = password or os.getenv("POSTGRESQL_PASSWORD")

        self.client = None
        self.cursor = None

        self.create_connection()

    def create_connection(self):
        self.logger.info(f"Create connection to {self.host}:{self.port}")

        self.client = psycopg2.connect(
            database=self.name,
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
        )
        # self.cursor = self.client.cursor()
        self.cursor = self.client.cursor(cursor_factory=extras.DictCursor)

    def fetch_rows(self, query: str):
        self.logger.info(f"Fetch rows from DB by query")
        self.cursor.execute(query)
        self.logger.debug(f"Finished to fetch rows by query")

        try:
            return self.cursor.fetchall()
        except psycopg2.ProgrammingError as e:
            raise psycopg2.ProgrammingError(f"Error executing query: {query}") from e
