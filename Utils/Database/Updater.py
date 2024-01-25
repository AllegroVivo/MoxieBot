from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Position, Trainer, Trainee, Qualification, Training, TUser, SignUpMessage, Job
    from Utils import RequirementLevel
################################################################################

__all__ = ("DatabaseUpdater",)

################################################################################
class DatabaseUpdater(DBWorkerBranch):
    """A utility class for updating records in the database."""

    pass
            
################################################################################
    
################################################################################
    