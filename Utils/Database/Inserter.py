from __future__ import annotations

from datetime import date, time
from typing import TYPE_CHECKING, Optional

from discord import User

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Position
    from Utils import CompensationType
################################################################################

__all__ = ("DatabaseInserter",)

################################################################################
class DatabaseInserter(DBWorkerBranch):
    """A utility class for inserting new records into the database."""

    pass
    # def insert_punch_card(self, patron_id: int) -> str:
    #     """Insert a new punch card record into the database."""
    # 
    #     new_id = self.generate_id()
    #     
    #     with self
            
################################################################################
    
################################################################################
    