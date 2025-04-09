from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Request


class TronRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_request(self, address: str):
        request = Request(address=address)
        self.db.add(request)
        await self.db.commit()
        await self.db.refresh(request)
        return request
    
    async def get_requests(self, limit: int, offset: int):
        s_query = (
            select(Request)
            .order_by(Request.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(s_query)
        return result.scalars().all()

    async def get_total_count(self):
        s_query = select(func.count()).select_from(Request)
        result = await self.db.execute(s_query)
        return result.scalar()
