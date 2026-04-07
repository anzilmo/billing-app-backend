from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    barcode: str
    price: float
    stock: int

class ProductResponse(BaseModel):
    id: int
    name: str
    barcode: str
    price: float
    stock: int

    class Config:
        from_attributes = True