from __future__ import annotations

from discord import Cog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes import MoxieBot
################################################################################
class Admin(Cog):
    
    def __init__(self, bot: MoxieBot):

        self.bot: MoxieBot = bot
        
################################################################################
def setup(bot: MoxieBot) -> None:

    bot.add_cog(Admin(bot))
    
################################################################################
