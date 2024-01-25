from __future__ import annotations

from discord import Interaction, User
from typing import TYPE_CHECKING, List

from .PunchCard import PunchCard

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("Patron", )

################################################################################
class Patron:
    
    __slots__ = (
        "_user",
        "_cards",
    )
    
################################################################################
    def __init__(self, user: User) -> None:
        
        self._user: User = user
        self._cards: List[PunchCard] = []
        
################################################################################
