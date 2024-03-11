from __future__ import annotations

import sys

from typing import TYPE_CHECKING, List, Optional, Any

from discord import Attachment, Bot, TextChannel, User, Interaction, NotFound, EmbedField

from Assets import BotImages
from .Patron import Patron
from .StaffManager import StaffManager
from Utils.Database import Database
from Utils import Utilities as U

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("MoxieBot",)

################################################################################
class MoxieBot(Bot):

    __slots__ = (
        "_image_dump",
        "database",
        "_patrons",
        "_weights",
        "_staff_mgr",
        "_error_channel",
    )

################################################################################
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._image_dump: TextChannel = None  # type: ignore
        self._error_channel: TextChannel = None  # type: ignore
        
        self.database: Database = Database(self)
        
        self._patrons: List[Patron] = []
        self._weights: List[int] = [45, 35, 15, 5]
        
        self._staff_mgr: StaffManager = StaffManager(self)

################################################################################
    async def on_error(self, event_method: str, *args: Any, **kwargs: Any) -> None:
        
        # exc = sys.exc_info()
        # error_type = exc[0]
        # error = exc[1]
        # traceback = exc[2]
        # 
        # embed = U.make_embed(
        #     title=f"`{error_type.__name__}` occurred!",
        #     description=f"```{error}```",
        # )
        # 
        # print(embed)
        # await self._error_channel.send(embed=embed)
        pass
        
################################################################################
    @property
    def staff_manager(self) -> StaffManager:
        
        return self._staff_mgr
    
################################################################################
    async def load_all(self) -> None:

        print("Fetching image dump...")
        self._image_dump = await self.fetch_channel(991902526188302427)
        self._error_channel = await self.fetch_channel(974493350919045190)

        print("Asserting database structure...")
        self.database._assert_structure()
        
        print("Loading data from database...")
        data = self.database._load_all()
                
        for patron in data["punches"]:
            try:
                user = await self.fetch_user(patron[0])
            except NotFound:
                continue
            self._patrons.append(Patron(self, user, patron[1], patron[2], patron[3]))
            
        print("Done!")

################################################################################
    async def dump_image(self, image: Attachment) -> str:

        file = await image.to_file()
        post = await self._image_dump.send(file=file)   # type: ignore

        return post.attachments[0].url

################################################################################
    def get_patron(self, user: User) -> Patron:
        
        patron = None
        
        for p in self._patrons:
            if p.user_id == user.id:
                patron = p

        if patron is None:
            patron = Patron(self, user)
            self.database.insert.insert_patron(user.id)
            self._patrons.append(patron)
            
        return patron
        
################################################################################
    async def stamp_member(self, interaction: Interaction, user: User, qty: int) -> None:
        
        patron = self.get_patron(user)            
        await patron.stamp(interaction, qty)

################################################################################
    async def view_user_stats(self, interaction: Interaction, user: User = None) -> None:
        
        patron = self.get_patron(user or interaction.user)
        await patron.view_stats(interaction)

################################################################################
    async def redeem_coin(self, interaction: Interaction) -> None:
        
        patron = self.get_patron(interaction.user)
        await patron.redeem(interaction)

################################################################################
    @staticmethod
    async def send_help(interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="__A Cat's Minion Gachapon Help__",
            description=(
                "Each visit earns you 1 stamp on your card!\n\n"
                
                "**When you reach 5 stamps you’ll earn ~A Cat’s Coin~!**\n"
                f"{U.draw_line(extra=33)}\n"
                "__Available Commands:__"
            ),
            fields=[
                EmbedField(
                    name="__/View Stamps__",
                    value="`View your current punch card stamps and stats.`",
                    inline=False
                ),
                EmbedField(
                    name="__/Redeem__",
                    value="`Use your coin on our gachapon and receive a minion capsule!`",
                    inline=False
                ),
                EmbedField(
                    "__/Help__",
                    "`That's this message!`",
                    False
                )
            ],
            thumbnail_url=BotImages.GameRules
        )
        
        await interaction.respond(embed=embed, ephemeral=True)

################################################################################
