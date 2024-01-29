from __future__ import annotations

from datetime import datetime
from discord import Interaction, User
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from Assets import BotImages, BotEmojis
from .GachaponMachine import GachaponMachine
from Utils import Utilities as U

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
        
        return self._punches >= 5
    
################################################################################
    @property
    def punches(self) -> int:
        
        return self._punches
    
################################################################################
    @property
    def redeem_date(self) -> Optional[datetime]:
        
        return self._redeem_date 

################################################################################    
    @redeem_date.setter
    def redeem_date(self, value: Optional[datetime]) -> None:
        
        self._redeem_date = value
        self.update()
        
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
                return BotImages.CardFull
            case 6:
                return BotImages.CardFull
            case _:
                return BotImages.CardBlank 
    
################################################################################
    async def punch(self, interaction: Interaction, qty: int) -> None:
        
        self._punches += qty
        self.update()
        
        await interaction.respond(f"Thanks for visiting, {self._parent.user.mention}! Here's your stamp!")
        await self.send_current_stamps(interaction)

################################################################################
    async def send_current_stamps(self, interaction: Interaction) -> None:

        await interaction.channel.send(self.current_image)
        await interaction.channel.send(
            f"You currently have **`~~ {self.punches} ~~`** punches on your card!"
        )

        if self._parent.coins > 0:
            await interaction.channel.send(
                f"You also have **`~~ {self._parent.coins} ~~`** coins to /redeem!"
            )

################################################################################
    def update(self) -> None:
        
        self.bot.database.update.punch_card(self)

################################################################################
    async def redeem(self, interaction: Interaction) -> None:
        
        machine = GachaponMachine()
        prize = await machine.play(interaction)
        self.redeem_date = datetime.now()
        
        await interaction.channel.send(U.draw_line(extra=22))
        
        header = (
            f"{BotEmojis.Gem}{BotEmojis.Gem} __**CONGRATULATIONS!**__ "
            f"{BotEmojis.Gem}{BotEmojis.Gem}"
        )
        await interaction.channel.send(header)
        await interaction.channel.send(prize.image)
        await interaction.channel.send(
            f"**{interaction.user.display_name} won a __`{prize.proper_name}`__ capsule!**\n"
            "A Cat's Staff will come by with your prize shortly."
        )
    
################################################################################
    