from discord import Cog, SlashCommandGroup, ApplicationContext, Option, SlashCommandOptionType
from typing import TYPE_CHECKING

from Classes.GachaponMachine import GachaponMachine

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
        ),
        quantity: Option(
            SlashCommandOptionType.integer,
            name="quantity",
            description="The number of punches to give",
            default=1,
            max_value=5
        )
    ) -> None:
        
        await self.bot.stamp_member(ctx.interaction, user, quantity)
 
################################################################################
    @admin.command(
        name="view",
        description="View a patron's punch stats",
    )
    async def view_stats(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="member",
            description="The member to view",
            required=True,
        )
    ) -> None:
        
        await self.bot.view_user_stats(ctx.interaction, user)
        
################################################################################
    @admin.command(
        name="capsules",
        description="Capsule test",
    )
    async def capsules(self, ctx: ApplicationContext) -> None:
        
        machine = GachaponMachine()
        await machine.play(ctx.interaction)
        
################################################################################
def setup(bot: "MoxieBot") -> None:

    bot.add_cog(Admin(bot))
    
################################################################################
