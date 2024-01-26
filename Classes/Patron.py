from __future__ import annotations

from discord import Interaction, User
from typing import TYPE_CHECKING, List

from Assets import BotImages
from .PunchCard import PunchCard

if TYPE_CHECKING:
    from Classes import MoxieBot
################################################################################

__all__ = ("Patron", )

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
    def get_current_card(self) -> PunchCard:
        
        ret = None
        
        for card in self._cards:
            if not card.is_complete:
                ret = card
                
        if ret is None:
            ret = self.create_card()
            
        return ret
    
################################################################################
    async def stamp(self, interaction: Interaction) -> None:
        
        card = self.get_current_card()
        await card.punch(interaction)
            
################################################################################
    def create_card(self) -> PunchCard:
        
        card = PunchCard.new(self)
        self._cards.append(card)
        
        return card

################################################################################
