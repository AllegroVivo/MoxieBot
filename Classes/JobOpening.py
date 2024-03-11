from __future__ import annotations

from datetime import datetime
from discord import Interaction, User
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from Assets import BotImages, BotEmojis
from .GachaponMachine import GachaponMachine
from Utils import Utilities as U

if TYPE_CHECKING:
    from Classes import Patron, MoxieBot, StaffManager, JobSlot
################################################################################

__all__ = ("JobOpening",)

PC = TypeVar("PC", bound="PunchCard")

################################################################################
class JobOpening:
    
    __slots__ = (
        "_state",
        "_slots",
        "_name",
        "_notes",
        "_emoji",
    )
    
################################################################################
    def __init__(
        self, 
        parent: StaffManager
    ) -> None:
        
        self._state: StaffManager = parent
        self._slots: List[JobSlot] = []
    
################################################################################
