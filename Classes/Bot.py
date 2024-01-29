from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from discord import Attachment, Bot, TextChannel, User, Interaction, NotFound, EmbedField

from Assets import BotImages
from Classes.Patron import Patron
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
        "_weights"
    )

################################################################################
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._image_dump: TextChannel = None  # type: ignore
        self.database: Database = Database(self)
        
        self._patrons: List[Patron] = []
        self._weights: List[int] = [45, 35, 15, 5]

################################################################################
    async def load_all(self) -> None:

        print("Fetching image dump...")
        self._image_dump = await self.fetch_channel(991902526188302427)

        print("Asserting database structure...")
        self.database.assert_structure()
        
        print("Loading data from database...")
        data = self.database.load_all()
        
        # Load stuff here
        punch_card_records = {}
        for record in data["punch_cards"]:
            try:
                punch_card_records[record[1]].append(record)
            except KeyError:
                punch_card_records[record[1]] = [record]
                
        for patron in punch_card_records:
            user = self.get_user(patron)
            if user is None:
                try:
                    user = await self.fetch_user(patron)
                except NotFound:
                    continue
        
            p = Patron.load(self, user, punch_card_records[patron])
            self._patrons.append(p)
            
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
        await patron.redeem_coin(interaction)

################################################################################
    @staticmethod
    async def send_help(interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="__A Cat's Minion Gachapon Help__",
            description=(
                "Each visit earns you 1 stamp on your card!\n\n"
                
                "**When you reach 6 stamps you’ll earn ~A Cat’s Coin~!**\n"
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
