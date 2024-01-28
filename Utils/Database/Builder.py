from __future__ import annotations

from .Branch import DBWorkerBranch
################################################################################

__all__ = ("DatabaseBuilder",)

################################################################################
class DatabaseBuilder(DBWorkerBranch):
    """A utility class for building and asserting elements of the database."""

    def build_all(self) -> None:

        self.build_punch_card_table()
        
        print("Database lookin' good!")
        
################################################################################
    def build_punch_card_table(self) -> None:
        
        with self.database as db:   
            db.execute(
                "CREATE TABLE IF NOT EXISTS punch_cards ("
                "_id TEXT PRIMARY KEY,"
                "user_id BIGINT NOT NULL,"
                "punches INTEGER DEFAULT 1,"
                "redeemed TIMESTAMP DEFAULT NULL"
                ");"
            )
            
################################################################################
