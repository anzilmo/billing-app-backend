from fastapi import APIRouter
from app.api.v1 import product
from app.api.v1 import invoice

router = APIRouter()

router.include_router(product.router)
router.include_router(invoice.router)