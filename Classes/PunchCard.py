from __future__ import annotations

from discord import Interaction, User
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from Classes import Patron
################################################################################

__all__ = ("PunchCard",)

################################################################################
class PunchCard:
    
    __slots__ = (
        "_id",
        "_parent",
        "_punches",
    )
    
################################################################################
    def __init__(self, _id: str, parent: Patron, punches: Optional[int] = None) -> None:
        
        _id: str = _id
        self._parent: Patron = parent
        
        self._punches: int = punches or 0
        
################################################################################
