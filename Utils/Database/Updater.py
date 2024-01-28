from __future__ import annotations

from typing import TYPE_CHECKING

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import PunchCard
################################################################################

__all__ = ("DatabaseUpdater",)

################################################################################
class DatabaseUpdater(DBWorkerBranch):
    """A utility class for updating records in the database."""

    def punch_card(self, pc: PunchCard) -> None:
        
        with self.database as db:
            db.execute(
                "UPDATE punch_cards SET punches = %s, redeemed = %s "
                "WHERE _id = %s;",
                (pc.punches, pc.redeem_date, pc.id)
            )
            
################################################################################
    
################################################################################
    