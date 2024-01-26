from discord import Cog, SlashCommandGroup, ApplicationContext, Option, SlashCommandOptionType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes import MoxieBot
################################################################################
class UserViewing(Cog):
    
    def __init__(self, bot: "MoxieBot"):

        self.bot: "MoxieBot" = bot
        
    
################################################################################    
    
    viewing = SlashCommandGroup(
        name="view",
        description="Commands for viewing stamp status."
    )
    
################################################################################
    @viewing.command(
        name="stamps",
        description="View your current punch card stamps",
    )    
    async def view_stamps(self, ctx: ApplicationContext) -> None:
        
        await self.bot.view_stamps(ctx.interaction)
 
################################################################################
def setup(bot: "MoxieBot") -> None:

    bot.add_cog(UserViewing(bot))
    
################################################################################
