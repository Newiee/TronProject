from unittest.mock import patch, AsyncMock
from src.main import app
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi.testclient import TestClient
from src.database.database import Base, get_db


@pytest.fixture()
async def db_session(scope="function"):
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    test_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with test_session as session:
        yield session
    await test_engine.dispose()

@pytest.fixture()
def client(db_session):
    def override_get_db():
        return db_session
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.mark.asyncio
async def test_post_tron_info(client):
    with patch ("src.services.tron_service.TronService.get_one") as mock_get_one:
        mock_get_one.return_value = {
            "balance_trx": 213.341,
            "bandwidth": {
                "freeNetUsed": 100,
                "freeNetLimit": 5000,
                "NetUsed": 200,
                "NetLimit": 1000
            },
            "energy": {
                "EnergyUsed": 300,
                "EnergyLimit": 2000
            }
        }

        response = client.post("/api/v1/tron_info/TNUC9Qb1rRpS5CbWLmNMxXBjyFoydXjWFR")

        assert response.status_code == 200
        data = response.json()
        assert data["balance_trx"] == 213.341
        assert data["bandwidth"]["freeNetUsed"] == 100
        assert data["bandwidth"]["freeNetLimit"] == 5000
        assert data["energy"]["EnergyUsed"] == 300
        assert data["energy"]["EnergyLimit"] == 2000

