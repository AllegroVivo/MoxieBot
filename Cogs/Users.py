from discord import (
    Cog, 
    SlashCommandGroup, 
    ApplicationContext, 
    slash_command,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes import MoxieBot
################################################################################
class UserViewing(Cog):
    
    def __init__(self, bot: "MoxieBot"):

        self.bot: "MoxieBot" = bot
    
################################################################################
    @slash_command(
        name="view_stamps",
        description="View your current punch card stamps",
    )    
    async def view_stamps(self, ctx: ApplicationContext) -> None:
        
        await self.bot.view_user_stats(ctx.interaction)
 
################################################################################
    @slash_command(
        name="redeem",
        description="Redeem a completed Cat's Coin!"
    )
    async def redeem(self, ctx: ApplicationContext) -> None:
        
        await self.bot.redeem_coin(ctx.interaction)
        
################################################################################
    @slash_command(
        name="help",
        description="View help information"
    )
    async def help(self, ctx: ApplicationContext) -> None:
        
        await self.bot.send_help(ctx.interaction)
        
################################################################################
def setup(bot: "MoxieBot") -> None:

    bot.add_cog(UserViewing(bot))
    
################################################################################
