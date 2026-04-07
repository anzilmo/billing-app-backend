from fastapi import APIRouter
from app.api.v1 import product

router = APIRouter()

router.include_router(product.router)