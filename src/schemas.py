from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field


class Bandwidth(BaseModel):
    freeNetUsed: int = Field(..., examples=[0])
    freeNetLimit: int = Field(..., examples=[3321])
    NetUsed: int = Field(..., examples=[0])
    NetLimit: int = Field(..., examples=[0])


class Energy(BaseModel):
    EnergyUsed: int = Field(..., examples=[0])
    EnergyLimit: int = Field(..., examples=[0])

class TronInfoSchema(BaseModel):
    balance_trx: float = Field(..., examples=[123.5])
    bandwidth: Bandwidth
    energy: Energy


class PagBase(BaseModel):
    current_page: int
    total_pages: int
    items_per_page: int
    total_items: int


class ResponseSchema(BaseModel):
    id: int = Field(..., examples=[1])
    address: str = Field(..., examples=['address'])
    created_at: datetime = Field(..., examples=["2008-09-15"])

    class Config:
        from_attributes = True

class PagResponse(PagBase):
    items: List[ResponseSchema]

class HTTPExceptionResponse(BaseModel):
    detail: str