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
            # "punch_cards": self.punch_cards(),
            "punches": self.punches(),
        }

################################################################################
    def punch_cards(self) -> Tuple[Tuple[Any, ...]]:
        """Returns a dictionary of punch cards."""

        self.execute("SELECT * FROM punch_cards;")
        return self.fetchall()
        
################################################################################
    def punches(self) -> Tuple[Tuple[Any, ...]]:
        """Returns a dictionary of punches."""

        self.execute("SELECT * FROM punches;")
        return self.fetchall()
    
################################################################################
