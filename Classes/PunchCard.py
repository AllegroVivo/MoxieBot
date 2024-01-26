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
        "_completion_date",
    )
    
################################################################################
    def __init__(
        self, 
        _id: str,
        parent: Patron, 
        punches: Optional[int] = None,
        completion_date: Optional[datetime] = None
    ) -> None:
        
        self._id: str = _id
        self._parent: Patron = parent
        
        self._punches: int = punches or 0
        self._completion_date: Optional[datetime] = completion_date
    
################################################################################
    @classmethod
    def new(cls: Type[PC], parent: Patron) -> PC:
        
        new_id = parent.bot.database.insert.punch_card(parent.user_id)
        return cls(new_id, parent)
    
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
    async def punch(self, interaction: Interaction) -> None:
        
        self._punches += 1
        if self._punches == 6:
            self._completion_date = datetime.now()
        
        self.update()
        
        await interaction.respond(f"{self._parent.user.mention} has arrived on the scene!")
        await self.send_current_stamps(interaction)

################################################################################
    async def send_current_stamps(self, interaction: Interaction) -> None:

        match self.punches:
            case 1:
                image_url = BotImages.Card1Stamp
            case 2:
                image_url = BotImages.Card2Stamp
            case 3:
                image_url = BotImages.Card3Stamp
            case 4:
                image_url = BotImages.Card4Stamp
            case 5:
                image_url = BotImages.Card5Stamp
            case 6:
                image_url = BotImages.CardFull
            case _:
                image_url = BotImages.CardBlank

        await interaction.channel.send(image_url)
        await interaction.channel.send(
            f"You currently have **`~~ {self.punches} ~~`** punches on your card!"
        )

################################################################################
    def update(self) -> None:
        
        self.bot.database.update.punch_card(self)

################################################################################
