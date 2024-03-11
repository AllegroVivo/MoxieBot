from __future__ import annotations

from discord import Cog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes import MoxieBot
################################################################################
class Internal(Cog):
    
    def __init__(self, bot: MoxieBot):

        self.bot: MoxieBot = bot
        
################################################################################
    @Cog.listener("on_ready")
    async def load_internals(self) -> None:

        print("Loading internals...")
        await self.bot.load_all()
        
        print("MoxieBot Online!")
        
################################################################################
def setup(bot: MoxieBot) -> None:

    bot.add_cog(Internal(bot))
    
################################################################################
