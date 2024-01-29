from enum import Enum
from typing import List

from discord import SelectOption, PartialEmoji

from Assets import BotEmojis, BotImages
################################################################################

__all__ = (
    "PrizeTier",
)

################################################################################
class FroggeEnum(Enum):
    
    @property
    def proper_name(self) -> str:
        
        return self.name
    
################################################################################    
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        raise NotImplementedError
        
################################################################################
    @property
    def select_option(self) -> SelectOption:

        return SelectOption(label=self.proper_name, value=str(self.value))

################################################################################
class PrizeTier(FroggeEnum):
    
    Common = 0
    Uncommon = 1
    Rare = 2
    Legendary = 3
    
################################################################################
    @classmethod
    def from_emoji_str(cls, emoji: str) -> "PrizeTier":
        
        if emoji == str(BotEmojis.CapsuleCommon):
            return cls.Common
        elif emoji == str(BotEmojis.CapsuleUncommon):
            return cls.Uncommon
        elif emoji == str(BotEmojis.CapsuleRare):
            return cls.Rare
        elif emoji == str(BotEmojis.CapsuleLegendary):
            return cls.Legendary
        else:
            raise ValueError(f"Invalid emoji string: {emoji}")

################################################################################
    @property
    def image(self) -> str:
        
        if self.value == 0:
            return BotImages.CapsuleCommon
        elif self.value == 1:
            return BotImages.CapsuleUncommon
        elif self.value == 2:
            return BotImages.CapsuleRare
        elif self.value == 3:
            return BotImages.CapsuleLegendary
        else:
            raise ValueError(f"Invalid prize tier: {self.value}")
    
################################################################################
    