import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.database.database import Base
from src.repositories.tron_repository import TronRepository


@pytest.mark.asyncio
async def test_create_request():
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    test_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async with test_session() as db:
        repository = TronRepository(db)
        address = "TNUC9Qb1rRpS5CbWLmNMxXBjyFoydXjWFR"

        created_request = await repository.create_request(address)

        assert created_request.address == address
        assert created_request.id is not None
        assert created_request.created_at is not None

        result = await db.execute(text(
            "SELECT * FROM requests WHERE address = :address"), {"address":address}
        )

        db_request = result.fetchone()
        assert db_request is not None
        assert db_request.address == address

    await test_engine.dispose()
