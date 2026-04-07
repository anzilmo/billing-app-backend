from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.product import Product
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem

from app.schemas.invoice import InvoiceCreate, InvoiceResponse

router = APIRouter(prefix="/api/v1/invoices", tags=["Invoices"])


@router.post("/", response_model=InvoiceResponse)
def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db)):
    total = 0
    invoice_items = []

    for item in data.items:
        product = db.query(Product).filter(Product.barcode == item.barcode).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.barcode} not found")

        item_total = product.price * item.quantity
        total += item_total

        invoice_items.append({
            "product": product,
            "quantity": item.quantity,
            "price": product.price
        })

    # create invoice
    new_invoice = Invoice(total_amount=total)
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    # save invoice items
    for item in invoice_items:
        db_item = InvoiceItem(
            invoice_id=new_invoice.id,
            product_id=item["product"].id,
            quantity=item["quantity"],
            price=item["price"]
        )
        db.add(db_item)

    db.commit()

    return {
        "id": new_invoice.id,
        "total_amount": total,
        "items": [
            {
                "product_id": item["product"].id,
                "quantity": item["quantity"],
                "price": item["price"]
            }
            for item in invoice_items
        ]
    }


@router.get("/")
def get_invoices(db: Session = Depends(get_db)):
    return db.query(Invoice).all()



@router.get("/{id}")
def get_invoice(id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    items = db.query(InvoiceItem).filter(InvoiceItem.invoice_id == id).all()

    return {
        "id": invoice.id,
        "total_amount": invoice.total_amount,
        "items": items
    }