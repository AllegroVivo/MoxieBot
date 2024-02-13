from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict

import psycopg2
from dotenv import load_dotenv
from psycopg2 import OperationalError, InterfaceError

from .Worker import DatabaseWorker

if TYPE_CHECKING:
    from psycopg2.extensions import connection, cursor

    from .Inserter import DatabaseInserter
    from .Updater import DatabaseUpdater
    from .Deleter import DatabaseDeleter
    from Classes.Bot import PartyBusBot
################################################################################

__all__ = ("Database", )

################################################################################
class Database:
    """Database class for handling all database interactions."""

    __slots__ = (
        "_state",
        "_connection",
        "_cursor",
        "_worker",
    )

################################################################################
    def __init__(self, bot: PartyBusBot):

        self._state: PartyBusBot = bot

        self._connection: connection = None  # type: ignore
        self._cursor: cursor = None  # type: ignore
        self._worker: DatabaseWorker = DatabaseWorker(bot)

################################################################################
    def __enter__(self) -> cursor:
    
        load_dotenv()
    
        self._connect()
        try:
            self._cursor.execute("SELECT 1")
        except OperationalError:
            self._reset_connection()
            self._connect()
    
        return self._cursor

################################################################################
    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
    
        self._reset_connection()

################################################################################
    def _reset_connection(self) -> None:
    
        try:
            self._cursor.close()
            self._connection.close()
        except OperationalError:
            pass
        finally:
            self._connection = None
            self._cursor = None

################################################################################        
    def _connect(self) -> None:

        self._connection = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
        self._cursor = self._connection.cursor()
        
################################################################################
    @property
    def connection(self) -> connection:

        return self.__connection

################################################################################
    @property
    def cursor(self) -> None:

        raise Exception(
            "Cursor is not a property of Database. Use a context manager block instead."
        )

################################################################################
    @property
    def insert(self) -> DatabaseInserter:

        return self._worker._inserter

################################################################################
    @property
    def update(self) -> DatabaseUpdater:

        return self._worker._updater

################################################################################

    @property
    def delete(self) -> DatabaseDeleter:

        return self._worker._deleter

################################################################################
    def assert_structure(self) -> None:

        self._worker.build_all()

################################################################################
    def load_all(self) -> Dict[str, Any]:

        return self._worker.load_all()

################################################################################
