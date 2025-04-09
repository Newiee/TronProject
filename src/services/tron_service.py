import logging

from fastapi import HTTPException
from tronpy import Tron
from tronpy.providers import HTTPProvider

from src.repositories.tron_repository import TronRepository
from src.schemas import TronInfoSchema, Bandwidth, Energy, PagResponse, ResponseSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TronService:
    def __init__(self, db):
        self.db = db
        self.repository = TronRepository(db)

    async def get_one(self, address: str) -> TronInfoSchema:
        provider = HTTPProvider(api_key="7cd0382b-2ce1-415e-abc4-c885df27c754")
        client = Tron(provider, network="mainnet")
        logger.info(f"Fetching info for tron wallet with address: {address}")
        try:
            balance = client.get_account_balance(address)
            resources = client.get_account_resource(address)
        except Exception as e:
            raise HTTPException(400 ,f"Unexpected error occurred: {e}")

        logger.info(f"Creating request in repo")
        await self.repository.create_request(address)

        return TronInfoSchema(
            balance_trx=balance,
            bandwidth=Bandwidth(
                freeNetUsed=resources.get("freeNetUsed", 0),
                freeNetLimit=resources.get("freeNetLimit", 0),
                NetUsed=resources.get("NetUsed", 0),
                NetLimit=resources.get("NetLimit", 0)
            ),
            energy=Energy(
                EnergyUsed=resources.get("EnergyUsed", 0),
                EnergyLimit=resources.get("EnergyLimit", 0)
            )
        )

    async def get_all(self, page: int, size: int) -> PagResponse:
        logger.info("Fetching data from db")
        offset = (page - 1) * size
        requests = await self.repository.get_requests(limit=size, offset=offset)
        total_items = await self.repository.get_total_count()
        total_pages = ((total_items or 0) + size - 1) // size

        items = [
            ResponseSchema(
                id=request.id,
                address=request.address,
                created_at=request.created_at
            )
            for request in requests
        ]

        return PagResponse(
            current_page=page,
            total_pages=total_pages,
            items_per_page=size,
            total_items=total_items,
            items=items,
        )