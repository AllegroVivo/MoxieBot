from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Tuple, List, Optional

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("DatabaseLoader",)

################################################################################
class DatabaseLoader(DBWorkerBranch):
    """A utility class for loading data from the database."""

    def load_all(self) -> Dict[str, Any]:
        """Performs all sub-loaders and returns a dictionary of their results."""

        return {
           "punch_cards": self.punch_cards(),
        }

################################################################################
    def punch_cards(self) -> Tuple[Tuple[str, int, int], ...]:
        """Returns a dictionary of punch cards."""

        with self.database as db:
            db.execute("SELECT * FROM punch_cards;")
            return db.fetchall()
        
################################################################################
