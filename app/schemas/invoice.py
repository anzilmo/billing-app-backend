from pydantic import BaseModel
from typing import List

class InvoiceItemCreate(BaseModel):
    barcode: str
    quantity: int

class InvoiceCreate(BaseModel):
    items: List[InvoiceItemCreate]


class InvoiceItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

class InvoiceResponse(BaseModel):
    id: int
    total_amount: float
    items: List[InvoiceItemResponse]

    class Config:
        from_attributes = True