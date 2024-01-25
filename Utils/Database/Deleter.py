from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Requirement, Training, Qualification
    from Utils import RequirementLevel
################################################################################

__all__ = ("DatabaseDeleter",)

################################################################################
class DatabaseDeleter(DBWorkerBranch):
    """A utility class for deleting data from the database."""
    
    pass
            
################################################################################

################################################################################
