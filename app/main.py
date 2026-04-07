from fastapi import FastAPI
from app.database import Base, engine
from app.models import Product, Invoice, InvoiceItem

from app.api import api_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Billing API is running 🚀"}

app.include_router(api_router)