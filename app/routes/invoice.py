from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from app.utils import get_db

router = APIRouter()

@router.post("/{user_id}")
def view_all_invoices_for_user(user_id: int, db: Session = Depends(get_db)):
    invoices = db.query(models.Invoice).filter(models.Invoice.user_id == user_id).all()
    if not invoices:
        return {"error": "No invoices found for this user"}
    return invoices

@router.get("/{user_id}/plan/{plan_id}")
def view_specified_invoice(user_id: int, plan_id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.user_id == user_id, models.Invoice.plan_id == plan_id).first()
    if not invoice:
        return {"error": "Invoice not found"}
    return invoice
