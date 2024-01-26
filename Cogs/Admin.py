from discord import Cog, SlashCommandGroup, ApplicationContext, Option, SlashCommandOptionType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes import MoxieBot
################################################################################
class Admin(Cog):
    
    def __init__(self, bot: "MoxieBot"):

        self.bot: "MoxieBot" = bot
        
    
################################################################################    
    
    admin = SlashCommandGroup(
        name="admin",
        description="Admin commands for MoxieBot"
    )
    
################################################################################
    @admin.command(
        name="stamp",
        description="Stamp a patron's punch card",
    )    
    async def stamp_card(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="member",
            description="The member to punch (Ouch!)",
            required=True,
        )
    ) -> None:
        
        await self.bot.stamp_member(ctx.interaction, user)
 
################################################################################
def setup(bot: "MoxieBot") -> None:

    bot.add_cog(Admin(bot))
    
################################################################################
