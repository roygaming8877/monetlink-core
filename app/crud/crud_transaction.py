from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate

class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    async def get_user_transactions(self, db: AsyncSession, *, user_id: str, skip: int = 0, limit: int = 50) -> List[Transaction]:
        """Retrieves withdrawal history for a specific user's invoice tab."""
        query = select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

transaction = CRUDTransaction(Transaction)
