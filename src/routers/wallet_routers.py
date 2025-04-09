from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.exceptions.exceptions import WalletNotFoundError
from src.schemas import TronInfoSchema, HTTPExceptionResponse, ResponseSchema, PagResponse
from src.services.tron_service import TronService

router = APIRouter()


@router.post(
    "/tron_info/{address}",
    response_model=TronInfoSchema,
    responses={
        404:{"model": HTTPExceptionResponse},
    },
)
async def get_one(address: str, db: AsyncSession = Depends(get_db)):
    service = TronService(db)
    try:
        return await service.get_one(address)
    except WalletNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )

@router.get("/requests", response_model=PagResponse)
async def get_all(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    service = TronService(db)
    return await service.get_all(page, size)