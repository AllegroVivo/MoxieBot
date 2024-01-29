from __future__ import annotations

import asyncio
import random
from typing import TYPE_CHECKING, List, Tuple

from discord import Interaction

from Assets import BotEmojis
from Utils import PrizeTier, edit_message_helper

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("GachaponMachine",)

################################################################################
class GachaponMachine:

    CAPSULES = [
        BotEmojis.CapsuleCommon,
        BotEmojis.CapsuleUncommon,
        BotEmojis.CapsuleRare,
        BotEmojis.CapsuleLegendary,
    ]
    
    __slots__ = (
        "_capsules",
    )
    
################################################################################
    def __init__(self) -> None:
        
        self._capsules: List[List[str]] = self._generate_capsule_grid()
    
################################################################################
    def _generate_capsule_grid(self) -> List[List[str]]:
        
        return [
            [str(random.choice(self.CAPSULES)) for _ in range(5)]
            for _ in range(5)
        ]
    
################################################################################
    def status(self) -> str:
        
        return "\n".join("".join(row) for row in self._capsules)
    
################################################################################
    async def play(self, interaction: Interaction) -> PrizeTier:
    
        msg = await interaction.channel.send(self.status())
    
        weights = [45, 35, 15, 5]
        chosen_capsule = str(random.choices(self.CAPSULES, weights, k=1)[0])
        pre_selected = self.pre_select_capsules(chosen_capsule, 3)
        replaceable_cells = [(i, j) for i in range(5) for j in range(5) if (i, j) not in pre_selected]
    
        while replaceable_cells:
            # Pick two random cells to replace in each iteration, if available
            for _ in range(min(2, len(replaceable_cells))):
                i, j = random.choice(replaceable_cells)
                self._capsules[i][j] = str(BotEmojis.CapsuleBlank)
                replaceable_cells.remove((i, j))
    
            await msg.edit(content=self.status())
            await asyncio.sleep(0.4)
            
        return PrizeTier.from_emoji_str(chosen_capsule)
                    
################################################################################
    def _get_capsules_by_type(self, capsule_type: str) -> List[Tuple[int, int]]:
        
        return [
            (row, col)
            for row, row_capsules in enumerate(self._capsules)
            for col, capsule in enumerate(row_capsules)
            if capsule == capsule_type
        ]
    
################################################################################
    def pre_select_capsules(self, capsule_type: str, qty: int) -> List[Tuple[int, int]]:
        
        try:
            return random.sample(self._get_capsules_by_type(capsule_type), qty)
        except ValueError:
            self._capsules = self._generate_capsule_grid()
            return self.pre_select_capsules(capsule_type, qty)
    
################################################################################
