from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from discord import Attachment, Bot, TextChannel, User, Interaction

from Classes.Patron import Patron
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
        "_patrons",
    )

################################################################################
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._image_dump: TextChannel = None  # type: ignore
        self.database: Database = Database(self)
        
        self._patrons: List[Patron] = []

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
    def get_patron_by_id(self, user_id: int) -> Optional[Patron]:
        
        for p in self._patrons:
            if p.user_id == user_id:
                return p
    
################################################################################    
    def get_patron(self, user: User) -> Patron:

        patron = self.get_patron_by_id(user.id)
        if patron is None:
            patron = Patron(self, user)
            self._patrons.append(patron)
            
        return patron
        
################################################################################
    async def stamp_member(self, interaction: Interaction, user: User) -> None:
        
        patron = self.get_patron(user)            
        await patron.stamp(interaction)

################################################################################
    async def view_stamps(self, interaction: Interaction) -> None:
        
        patron = self.get_patron(interaction.user)   
        await patron.send_current_stamps(interaction)

################################################################################
