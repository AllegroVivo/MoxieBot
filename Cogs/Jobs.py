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
class Jobs(Cog):
    
    def __init__(self, bot: "MoxieBot"):

        self.bot: "MoxieBot" = bot
        
################################################################################
    
    jobs = SlashCommandGroup(
        name="jobs",
        description="Commands for job posting-related tasks and queries"
    )

################################################################################
def setup(bot: "MoxieBot") -> None:

    bot.add_cog(Jobs(bot))
    
################################################################################
