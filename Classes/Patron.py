from __future__ import annotations

from discord import Interaction, User, Embed, EmbedField
from typing import TYPE_CHECKING, List, Type, TypeVar, Tuple, Optional

from Assets import BotImages
from .PunchCard import PunchCard

from UI import ConfirmCancelView
from Utils import Utilities as U, NoCoinsAvailableError

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
    )
    
################################################################################
    def __init__(self, state: MoxieBot, user: User) -> None:
        
        self._state: MoxieBot = state
        self._user: User = user
        
        self._cards: List[PunchCard] = []
    
################################################################################
    @classmethod
    def load(cls: Type[P], state: MoxieBot, user: User, data: List[Tuple[str, int, int]]) -> P:
        
        self: P = cls.__new__(cls)
        
        self._state = state
        self._user = user
        
        self._cards = [PunchCard(self, card[0], card[2], card[3]) for card in data]
        
        return self
        
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
    def cards(self) -> List[PunchCard]:
        
        return self._cards
    
################################################################################
    @property
    def coins(self) -> int:
        
        return len(
            [
                card for card in self._cards 
                if card.is_complete and card.redeem_date is None
            ]
        )
    
################################################################################
    def get_current_card(self) -> Optional[PunchCard]:

        for card in self._cards:
            if not card.is_complete:
                return card
    
################################################################################
    def get_unredeemed_card(self) -> Optional[PunchCard]:
        
        for card in self._cards:
            if card.is_complete and card.redeem_date is None:
                return card
            
################################################################################
    async def stamp(self, interaction: Interaction, qty: int) -> None:
        
        card = self.get_current_card()
        if card is None:
            card = self.create_card()
            
        qty = min(5 - card.punches, qty)
        await card.punch(interaction, qty)
            
################################################################################
    def create_card(self) -> PunchCard:
        
        card = PunchCard.new(self)
        self._cards.append(card)
        
        return card

################################################################################
    def status(self) -> Embed:
        
        completed_cards = [card for card in self._cards if card.is_complete]
        unredeemed_cards = [card for card in completed_cards if card.redeem_date is None]
        
        fields = [
            EmbedField(
                name="Current Punches",
                value=f"**`{self.get_current_card().punches if self.get_current_card() is not None else 0}`**",
                inline=True
            ),
            EmbedField(
                name="Available Coins",
                value=f"**`{len(unredeemed_cards)}`**",
                inline=True
            ),
            EmbedField(
                name="Completed Cards",
                value=f"**`{len(completed_cards)}`**",
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
            thumbnail_url=(
                card.current_image if (card := self.get_current_card()) is not None 
                else BotImages.CardBlank
            ),
            fields=fields
        )
    
################################################################################
    async def view_stats(self, interaction: Interaction) -> None:
        
        await interaction.respond(embed=self.status())

################################################################################
    async def redeem_coin(self, interaction: Interaction) -> None:
        
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
        
        card = self.get_unredeemed_card()
        await card.redeem(interaction)

################################################################################
