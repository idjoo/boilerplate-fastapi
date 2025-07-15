from sqlalchemy import select

from src.dependencies import Database


class HealthRepository:
    db: Database

    def __init__(self, db: Database) -> None:
        self.db = db

    async def check(
        self,
    ) -> bool:
        try:
            await self.db.exec(select(1))
            return True
        except:
            return False
