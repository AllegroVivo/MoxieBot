from __future__ import annotations

from uuid import uuid4
from typing import TYPE_CHECKING, Tuple, Any

if TYPE_CHECKING:
    from Classes.Bot import PartyBusBot
    from Utils import Database
################################################################################

__all__ = ("DBWorkerBranch",)

################################################################################
class DBWorkerBranch:
    """Common superclass for all Database-related workers. Basically just
    holds a reference to the bot."""

    __slots__ = (
        "_state",
    )

################################################################################
    def __init__(self, _state: PartyBusBot):

        self._state: PartyBusBot = _state

################################################################################
    @property
    def bot(self) -> PartyBusBot:

        return self._state

################################################################################
    @property
    def database(self) -> Database:

        return self._state.database

################################################################################
    @staticmethod
    def generate_id() -> str:
        
        return uuid4().hex
    
################################################################################
    def execute(self, query: str, *args) -> None:
        """Execute a query on the database."""

        self.database.execute(query, *args)
            
################################################################################
    def fetchall(self) -> Tuple[Tuple[Any, ...]]:

        return self.database.fetchall()

################################################################################
    def fetchone(self) -> Tuple[Any, ...]:

        return self.database.fetchone()

################################################################################
