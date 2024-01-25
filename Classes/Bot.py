from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Attachment, Bot, TextChannel

from Utils.Database import Database

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("MoxieBot",)

################################################################################
class MoxieBot(Bot):

    __slots__ = (
        "_image_dump",
        "database",
    )

################################################################################
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._image_dump: TextChannel = None  # type: ignore
        self.database: Database = Database(self)

################################################################################
    async def load_all(self) -> None:

        print("Fetching image dump...")
        self._image_dump = await self.fetch_channel(991902526188302427)

        print("Asserting database structure...")
        self.database.assert_structure()
        
        print("Loading data from database...")
        data = self.database.load_all()
        
        # Load stuff here

        print("Done!")

################################################################################
    async def dump_image(self, image: Attachment) -> str:

        file = await image.to_file()
        post = await self._image_dump.send(file=file)   # type: ignore

        return post.attachments[0].url

################################################################################
