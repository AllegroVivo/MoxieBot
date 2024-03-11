from __future__ import annotations

from datetime import datetime
from discord import Interaction, User
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from Assets import BotImages, BotEmojis
from .GachaponMachine import GachaponMachine
from Utils import Utilities as U

if TYPE_CHECKING:
    from Classes import Patron, MoxieBot, StaffManager
################################################################################

__all__ = ("JobSlot",)

PC = TypeVar("PC", bound="PunchCard")

################################################################################
class JobSlot:
    
    __slots__ = (
        "_state",
        "_user",
        "_sign_up_date",
        "_confirmed",
    )
    
################################################################################
    def __init__(
        self, 
        parent: StaffManager,
        user: Optional[User] = None,
        sign_up_date: Optional[datetime] = None,
        confirmed: Optional[datetime] = None
    ) -> None:
        
        self._state: StaffManager = parent
        
        self._user: Optional[User] = user
        self._sign_up_date: Optional[datetime] = sign_up_date
        self._confirmed: Optional[datetime] = confirmed
    
################################################################################
