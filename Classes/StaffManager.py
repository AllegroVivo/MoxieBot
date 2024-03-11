from __future__ import annotations

from datetime import datetime
from discord import Interaction, User
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from Assets import BotImages, BotEmojis
from .GachaponMachine import GachaponMachine
from Utils import Utilities as U

if TYPE_CHECKING:
    from Classes import Patron, MoxieBot, JobOpening
################################################################################

__all__ = ("StaffManager",)

PC = TypeVar("PC", bound="PunchCard")

################################################################################
class StaffManager:
    
    __slots__ = (
        "_state",
        "_jobs",
    )
    
################################################################################
    def __init__(
        self, 
        state: MoxieBot
    ) -> None:
        
        self._state: MoxieBot = state
        self._jobs: List[JobOpening] = []
    
################################################################################
    async def add_job(self, interaction: Interaction) -> None:
        
        pass
    
################################################################################
