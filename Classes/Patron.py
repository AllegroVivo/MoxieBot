from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, TypeVar

from discord import Interaction, User, Embed, EmbedField

from Assets import BotImages, BotEmojis
from UI import ConfirmCancelView
from Utils import Utilities as U, NoCoinsAvailableError
from .GachaponMachine import GachaponMachine
from .PunchCard import PunchCard

if TYPE_CHECKING:
    from Classes import MoxieBot
################################################################################

__all__ = ("Patron", )

P = TypeVar("P", bound="Patron")

################################################################################
class Patron:
    
    __slots__ = (
        "_state",
        "_user",
        "_cards",
        "_stamps",
        "_coins",
        "_redemptions",
    )
    
################################################################################
    def __init__(
        self,
        state: MoxieBot,
        user: User,
        stamps: int = 0,
        coins: int = 0,
        redemptions: int = 0
    ) -> None:
        
        self._state: MoxieBot = state
        self._user: User = user
        
        self._cards: List[PunchCard] = []
        
        self._stamps: int = stamps
        self._coins: int = coins
        self._redemptions: int = redemptions
    
################################################################################  
    @property
    def bot(self) -> MoxieBot:
        
        return self._state
    
################################################################################
    @property
    def user(self) -> User:
        
        return self._user
    
################################################################################
    @property
    def user_id(self) -> int:
        
        return self._user.id
    
################################################################################
    @property
    def stamps(self) -> int:
        
        return self._stamps
    
################################################################################
    @property
    def coins(self) -> int:
        
        return self._coins
    
################################################################################
    @property
    def redemptions(self) -> int:
        
        return self._redemptions
    
################################################################################
    @property
    def current_image(self) -> str:

        image = BotImages.CardBlank
        if self.stamps > 0:
            if self.stamps == 1:
                image = BotImages.Card1Stamp
            elif self.stamps == 2:
                image = BotImages.Card2Stamp
            elif self.stamps == 3:
                image = BotImages.Card3Stamp
            elif self.stamps == 4:
                image = BotImages.Card4Stamp
            else:
                image = BotImages.CardFull
                
        return image
         
################################################################################
    async def stamp(self, interaction: Interaction, qty: int) -> None:
        
        self._stamps += qty
        
        while self._stamps >= 5:
            self._coins += 1
            self._stamps -= 5

        self.update()

        await interaction.respond(f"Thanks for visiting, {self.user.display_name}! Here's your stamp!")
        await self.send_current_stamps(interaction)
        
################################################################################    
    def update(self) -> None:
        
        self.bot.database.update.punches(self)
        
################################################################################
    async def send_current_stamps(self, interaction: Interaction) -> None:

        await interaction.channel.send(self.current_image)
        await interaction.channel.send(
            f"You currently have **`~~ {self.stamps} ~~`** punches on your card!"
        )

        if self.coins > 0:
            await interaction.channel.send(
                f"{self.user.mention}\n"
                f"You also have **`~~ {self.coins} ~~`** coins to </redeem:1201661594678067281>!"
            )

################################################################################
    def status(self) -> Embed:
        
        fields = [
            EmbedField(
                name="Current Punches",
                value=f"**`{self.stamps}`**",
                inline=True
            ),
            EmbedField(
                name="Available Coins",
                value=f"**`{self.coins}`**",
                inline=True
            ),
            EmbedField(
                name="Completed Cards",
                value=f"**`{self.redemptions}`**",
                inline=True
            ),
            # EmbedField(
            #     name="Redemption History",
            #     value="`Coming Soon`:tm:",
            #     inline=False
            # )
        ]
        
        return U.make_embed(
            title=f"__{self._user.display_name}'s__ Punch Cards",
            description=U.draw_line(extra=32),
            thumbnail_url=self.current_image,
            fields=fields
        )
    
################################################################################
    async def view_stats(self, interaction: Interaction) -> None:
        
        await interaction.respond(embed=self.status())

################################################################################
    async def redeem(self, interaction: Interaction) -> None:

        if self.coins == 0:
            error = NoCoinsAvailableError()
            await interaction.respond(embed=error, ephemeral=True)
            return

        confirm = U.make_embed(
            title="Redeem Coin",
            description=(
                f"Are you sure you want to redeem a coin?\n"
                f"You currently have **`{self.coins}`** available."
            ),
            thumbnail_url=BotImages.CatCoin,
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=confirm, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return
        
        self._coins -= 1
        self._redemptions += 1
        self.update()

        machine = GachaponMachine()
        prize = await machine.play(interaction)

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
    