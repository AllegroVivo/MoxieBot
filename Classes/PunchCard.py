from __future__ import annotations

from datetime import datetime
from discord import Interaction, User
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from Assets import BotImages

if TYPE_CHECKING:
    from Classes import Patron, MoxieBot
################################################################################

__all__ = ("PunchCard",)

PC = TypeVar("PC", bound="PunchCard")

################################################################################
class PunchCard:
    
    __slots__ = (
        "_id",
        "_parent",
        "_punches",
        "_redeem_date",
    )
    
################################################################################
    def __init__(
        self, 
        parent: Patron, 
        _id: str,
        punches: Optional[int] = None,
        completion_date: Optional[datetime] = None
    ) -> None:
        
        self._id: str = _id
        self._parent: Patron = parent
        
        self._punches: int = punches or 0
        self._redeem_date: Optional[datetime] = completion_date
    
################################################################################
    @classmethod
    def new(cls: Type[PC], parent: Patron) -> PC:
        
        new_id = parent.bot.database.insert.punch_card(parent.user_id)
        return cls(parent, new_id)
    
################################################################################
    @property
    def bot(self) -> MoxieBot:
        
        return self._parent.bot

################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################    
    @property
    def is_complete(self) -> bool:
        
        return self._punches >= 6
    
################################################################################
    @property
    def punches(self) -> int:
        
        return self._punches
    
################################################################################
    @property
    def redeem_date(self) -> Optional[datetime]:
        
        return self._redeem_date 
    
################################################################################
    @property
    def current_image(self) -> str:

        match self.punches:
            case 1:
                return BotImages.Card1Stamp
            case 2:
                return BotImages.Card2Stamp
            case 3:
                return BotImages.Card3Stamp
            case 4:
                return BotImages.Card4Stamp
            case 5:
                return BotImages.Card5Stamp
            case 6:
                return BotImages.CardFull
            case _:
                return BotImages.CardBlank 
    
################################################################################
    async def punch(self, interaction: Interaction, qty: int) -> None:
        
        self._punches += qty
        self.update()
        
        await interaction.respond(f"{self._parent.user.mention} has arrived on the scene!")
        await self.send_current_stamps(interaction)

################################################################################
    async def send_current_stamps(self, interaction: Interaction) -> None:

        await interaction.channel.send(self.current_image)
        await interaction.channel.send(
            f"You currently have **`~~ {self.punches} ~~`** punches on your card!"
        )

################################################################################
    def update(self) -> None:
        
        self.bot.database.update.punch_card(self)

################################################################################
